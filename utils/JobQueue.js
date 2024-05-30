import Bull from "bull";
import dotenv from "dotenv";
import { spawn } from "child_process";
import { Proxy } from "../models/Proxy.js";
import axios from "axios";

dotenv.config();

const jobQueues = {};

const setup = async () => {
  // const proxies = [
  //   {
  //     key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
  //   },
  // ];
  const proxies = await Proxy.find({});
  proxies.forEach(
    (proxy) =>
      (jobQueues[proxy.key] = new Bull(`${proxy.key}-jobQueue`, {
        redis: {
          host: process.env.REDIS_HOST, // e.g., '127.0.0.1'
          port: process.env.REDIS_PORT, // e.g., 6379
        },
      }))
  );

  await Promise.all(
    proxies.map(async (proxy) => await jobQueues[proxy.key].empty())
  );

  proxies.forEach((proxy) => jobQueues[proxy.key].process(processJob));
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
  const maxBackoff = 32000;
  const proxy = await Proxy.findOne({ key: params["key"] });
  // const result = await axios.post(
  //   "http://localhost:8080/2015-03-31/functions/function/invocations",
  //   {
  //     body: {
  //       function_name: functionName,
  //       params: params,
  //       proxy: proxy,
  //     },
  //   }
  // );
  let result;
  try {
    result = await axios.post(
      "https://uukusuutzb.execute-api.us-west-1.amazonaws.com/default/LambdaPlaywright",
      {
        function_name: functionName,
        params: params,
        proxy: proxy,
      }
    );
  } catch (error) {
    // if (error.response && error.response.status === 503) {
    //   await new Promise((resolve) =>
    //     setTimeout(
    //       resolve,
    //       Math.min(
    //         Math.pow(2, retries) * 1000 + Math.random() * 1000,
    //         maxBackoff
    //       )
    //     )
    //   );
    //   result = { data: await runLambda(functionName, params, retries + 1) };
    // } else {
      throw error;
    // }
  }

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
          console.error(`Job failed`, error);
          reject(error);
        });
      return;
    }
    jobQueue
      .add({
        functionName,
        params,
      })
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
