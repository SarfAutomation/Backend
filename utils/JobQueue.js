import Bull from "bull";
import dotenv from "dotenv";
import { spawn } from "child_process";
import { Proxy } from "../models/Proxy.js";
import axios from "axios";

dotenv.config();

const jobQueues = {};

const setup = async () => {
  const proxies = await Proxy.find({});
  await Promise.all(
    proxies.map(async (proxy) => {
      const jobQueue = new Bull(`${proxy.key}-jobQueue`, {
        redis: {
          host: process.env.REDIS_HOST,
          port: process.env.REDIS_PORT,
          password: process.env.REDIS_PASSWORD,
        },
      });
      jobQueues[proxy.key] = jobQueue;
      await jobQueue.empty();
      jobQueue.process(processJob);
    })
  );
};

const runPythonFile = async (functionName, params) => {
  const proxy = await Proxy.findOne({ key: params["key"] });
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn("python3.11", [
      "-u",
      "./app/local_app.py",
      "-function",
      functionName,
      "-params",
      JSON.stringify(params),
      "-proxy",
      JSON.stringify(proxy),
    ]);

    let result = "";

    pythonProcess.stdout.on("data", (data) => {
      console.log(data.toString());
      result += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      console.error(`stderr: ${data}`);
    });

    pythonProcess.on("close", async (code) => {
      if (code === 0) {
        try {
          resolve(JSON.parse(result));
        } catch {
          resolve();
        }
      } else {
        reject(`Process failed with code ${code}`);
      }
    });
  });
};

const runLambda = async (functionName, params, retries = 0) => {
  const proxy = await Proxy.findOne({ key: params["key"] });
  let result;
  result = await axios.post(
    "https://hpmaekrvlqhaffzdxu4qeusqiq0qffgo.lambda-url.us-west-1.on.aws/",
    {
      function_name: functionName,
      params: params,
      proxy: proxy,
    }
  );
  return result.data;
};

const processJob = async (job) => {
  const { functionName, params } = job.data;
  // return await runPythonFile(functionName, params);
  return await runLambda(functionName, params);
};

async function scheduleJob(functionName, params) {
  return new Promise((resolve, reject) => {
    let jobQueue = jobQueues[params["key"]];
    console.log(jobQueue)
    if (!jobQueue) {
      processJob({
        data: {
          functionName,
          params,
        },
      })
        .then((result) => {
          resolve(result);
        })
        .catch((error) => {
          console.error(`Job failed:`, error);
          reject(error);
        });
      return;
    }
    jobQueue
      .add(
        {
          functionName,
          params,
        },
        { lifo: true }
      )
      .then((job) => {
        job
          .finished()
          .then(async (result) => {
            console.log(`Job ${job.id} completed`);
            resolve(result);
          })
          .catch((error) => {
            console.error(`Job ${job.id} failed`, error);
            reject(error);
          });
      })
      .catch((error) => {
        console.error(`Failed to add job to the queue`, error);
        reject(error);
      });
  });
}

export { scheduleJob, setup };
