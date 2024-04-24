import Bull from "bull";
import dotenv from "dotenv";
import { spawn } from "child_process";
import { Proxy } from "../models/Proxy.js";

dotenv.config();

const jobQueues = {};

const setup = async () => {
  const proxies = [
    {
      key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
    },
  ];
  // const proxies = await Proxy.find({});
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

const runPythonFile = async (params) => {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn("python3.11", params);

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

const processJob = async (job) => {
  const { params } = job.data;
  return await runPythonFile(params);
};

async function scheduleJob(params, key) {
  return new Promise((resolve, reject) => {
    jobQueues[
      "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G"
    ]
      // jobQueues[key]
      .add({
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
          });
      })
      .catch((error) => {
        console.error(`Failed to add job to the queue`, error);
      });
  });
}

export { scheduleJob, setup };
