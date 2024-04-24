import Bull from "bull";
import dotenv from "dotenv";
import { spawn } from "child_process";
import { Flow } from "../models/Flow.js";
import { Proxy } from "../models/Proxy.js";

dotenv.config();

const jobQueues = {};

const setup = async () => {
  const proxies = [
    {
      account:
        "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
    },
  ];
  proxies.forEach(
    (proxy) =>
      (jobQueues[proxy.account] = new Bull(`${proxy.account}-jobQueue`, {
        redis: {
          host: process.env.REDIS_HOST, // e.g., '127.0.0.1'
          port: process.env.REDIS_PORT, // e.g., 6379
        },
      }))
  );

  await Promise.all(
    proxies.map(async (proxy) => await jobQueues[proxy.account].empty())
  );

  proxies.forEach((proxy) => jobQueues[proxy.account].process(processJob));
};

const runPythonFile = async (params) => {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn("python3.11", params);

    let dataList = [];

    pythonProcess.stdout.on("data", (data) => {
      dataList.push(data.toString());
    });

    pythonProcess.stderr.on("data", (data) => {
      console.error(`stderr: ${data}`);
    });

    pythonProcess.on("close", async (code) => {
      if (code === 0) {
        resolve(JSON.parse(dataList));
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

async function scheduleJob(params) {
  return new Promise((resolve, reject) => {
    jobQueues[
      "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G"
    ]
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
