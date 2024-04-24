import express from "express";
import dotenv from "dotenv";
import { Proxy } from "../models/Proxy.js";
import { scheduleJob } from "../utils/JobQueue.js";
import { spawn } from "child_process";
import axios from "axios";

dotenv.config();
const router = express.Router();

router.post("/check-sales-nav-reply", async (req, res) => {
  try {
    const { profile, name } = req.body;
    const job = async () => {
      const data = await scheduleJob([
        "-u",
        "./automations/get_inmail.py",
        "-n",
        name,
      ]);
      const replies = data.messages.filter((message) => message.name != "You");
      if (replies.length) {
        await scheduleJob([
          "-u",
          "./automations/add_sales_nav_note.py",
          "-p",
          profile,
          "-n",
          "REPLIED",
        ]);
      }
      await axios.post(
        "https://hooks.zapier.com/hooks/catch/18369368/3nvau6i/",
        {
          hasReplied: replies.length > 0,
          replies,
          url: data.url,
        }
      );
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/send-LPA-inmail", async (req, res) => {
  try {
    const { profile, message, index } = req.body;
    const job = async () => {
      await scheduleJob([
        "-u",
        "./automations/send_inmail.py",
        "-p",
        profile,
        "-m",
        message,
        "-s",
        "",
      ]);
      await axios.post(
        "https://hooks.zapier.com/hooks/catch/18369368/3nvgssv/",
        {
          profile,
          index,
        }
      );
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/send-IC-inmail", async (req, res) => {
  try {
    const { profile, subject, message, index } = req.body;
    const job = async () => {
      await scheduleJob([
        "-u",
        "./automations/send_inmail.py",
        "-p",
        profile,
        "-m",
        message,
        "-s",
        subject,
      ]);
      await axios.post(
        "https://hooks.zapier.com/hooks/catch/18369368/37y1bdp/",
        {
          profile,
          index,
        }
      );
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/check-connection", async (req, res) => {
  try {
    const job = async () => {
      const data = await scheduleJob([
        "-u",
        "./automations/get_recent_connections.py",
      ]);
      const salesNavUrls = [];
      for (const linkedinUrl of data.slice(0, 2)) {
        const salesNavUrl = await scheduleJob([
          "-u",
          "./automations/get_sales_nav_url.py",
          "-l",
          linkedinUrl,
        ]);
        await axios.post(
          "https://hooks.zapier.com/hooks/catch/18369368/3nvym70/",
          {
            salesNavUrls,
          }
        );
        salesNavUrls.push(salesNavUrl);
      }
      console.log(salesNavUrls);
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/connect-from-search", async (req, res) => {
  try {
    const { searchUrl, message } = req.body;
    const job = async () => {
      const profiles = await scheduleJob([
        "-u",
        "./automations/search_sales_nav.py",
        "-s",
        searchUrl,
      ]);
      for (const profile of profiles) {
        const { url, isOpen } = profile;
        const { name, crSent } = await scheduleJob([
          "-u",
          "./automations/request_connect_sales_nav.py",
          "-p",
          url,
          "-m",
          message,
        ]);
        if (crSent) {
          await scheduleJob([
            "-u",
            "./automations/add_sales_nav_note.py",
            "-p",
            url,
            "-n",
            "New Connection",
          ]);
          await scheduleJob([
            "-u",
            "./automations/add_sales_nav_list.py",
            "-p",
            url,
            "-l",
            "CR Sent",
          ]);
          if (isOpen) {
            await axios.post(
              "https://hooks.zapier.com/hooks/catch/18369368/373nvju/",
              { name, url }
            );
          }
        }
      }
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.get("/get-proxy/:account", async (req, res) => {
  try {
    const { account } = req.params;
    const proxy = await Proxy.findOne({ account });
    return res.status(200).send({ proxy });
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

export default router;
