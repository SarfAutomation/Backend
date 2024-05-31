import express from "express";
import dotenv from "dotenv";
import { Proxy } from "../models/Proxy.js";
import { scheduleJob } from "../utils/JobQueue.js";
import { spawn } from "child_process";
import axios from "axios";
import { stringify } from "querystring";

dotenv.config();
const router = express.Router();

router.post("/check-IC-reply", async (req, res) => {
  try {
    const { profile, name } = req.body;
    const job = async () => {
      try {
        const callbackUrl =
          "https://hooks.zapier.com/hooks/catch/18369368/37u8r8a/";
        const data = await scheduleJob("get_inmail", {
          name: name,
          key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
        });
        const replies = data.messages.filter(
          (message) => message.name != "You"
        );
        if (replies.length) {
          await scheduleJob("add_sales_nav_note", {
            profile_link: profile,
            note: "REPLIED",
            key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
          });
        }
        await axios.post(callbackUrl, {
          hasReplied: replies.length > 0,
          replies,
          url: data.url,
        });
      } catch (error) {
        console.log("check-sales-nav-reply ERROR:", error);
      }
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/check-LPA-reply", async (req, res) => {
  try {
    const { profile, name } = req.body;
    const job = async () => {
      try {
        const callbackUrl =
          "https://hooks.zapier.com/hooks/catch/18369368/3nvau6i/";
        const inmailData = await scheduleJob("get_inmail", {
          name: name,
          key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
        });
        const inmailReplies = inmailData.messages.filter(
          (message) => message.name != "You"
        );
        const dmData = await scheduleJob("get_dm", {
          name: name,
          key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
        });
        const dmReplies = dmData.messages.filter(
          (message) => message.name != "You"
        );
        const replies = [...inmailReplies, ...dmReplies];
        if (replies.length) {
          await scheduleJob("add_sales_nav_note", {
            profile_link: profile,
            note: "REPLIED",
            key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
          });
        }
        // await axios.post(callbackUrl, {
        //   hasReplied: replies.length > 0,
        //   replies,
        //   url: dmData.url + "\n" + inmailData.url,
        // });
      } catch (error) {
        console.log("check-sales-nav-reply ERROR:", error);
      }
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
      try {
        await scheduleJob("send_inmail", {
          profile_link: profile,
          message: message,
          subject: "",
          key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
        });
        await axios.post(
          "https://hooks.zapier.com/hooks/catch/18369368/3nvgssv/",
          {
            profile,
            index,
          }
        );
      } catch (error) {
        console.log("send-LPA-inmail ERROR:", error);
      }
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
      try {
        await scheduleJob("send_inmail", {
          profile_link: profile,
          messaeg: message,
          subject: subject,
          key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
        });
        await axios.post(
          "https://hooks.zapier.com/hooks/catch/18369368/37y1bdp/",
          {
            profile,
            index,
          }
        );
      } catch (error) {
        console.log("send-IC-inmail ERROR:", error);
      }
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
      try {
        const data = await scheduleJob("get_recent_connections", {
          key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
        });
        console.log(data);
        await Promise.all(
          data.map(async (linkedinUrl) => {
            let salesNavUrl;
            try {
              salesNavUrl = await scheduleJob("get_sales_nav_url", {
                linkedin_url: linkedinUrl,
                key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
              });
            } catch (error) {
              return;
            }
            // if (salesNavUrl.name && salesNavUrl.url) {
            //   await axios.post(
            //     "https://hooks.zapier.com/hooks/catch/18369368/3nvym70/",
            //     {
            //       salesNavUrl,
            //     }
            //   );
            // }
          })
        );
      } catch (error) {
        console.log("check-connection ERROR:", error);
      }
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
      try {
        const profiles = await scheduleJob("search_sales_nav", {
          search_url: searchUrl,
          key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
        });
        for (const profile of profiles) {
          try {
            const { name, url, isOpen } = profile;
            const finalMessage = message.replace("NAME", name.split(" ")[0]);
            const { crSent } = await scheduleJob("request_connect_sales_nav", {
              profile_url: url,
              message: finalMessage,
              key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
            });
            if (crSent) {
              await scheduleJob("add_sales_nav_note", {
                profile_url: url,
                note: "New Connection",
                key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
              });
              await scheduleJob("add_sales_nav_list", {
                profile_url: url,
                list: "CR Sent",
                key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
              });
              if (isOpen) {
                await axios.post(
                  "https://hooks.zapier.com/hooks/catch/18369368/373nvju/",
                  { name, url }
                );
              }
              await axios.post(
                "https://hooks.zapier.com/hooks/catch/18369368/372rzbo/"
              );
            }
          } catch (error) {
            console.log(error);
          }
        }
      } catch (error) {
        console.log("connect-from-search ERROR:", error);
      }
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/find-post-and-comment", async (req, res) => {
  const { linkedinUrl, commentedPosts } = req.body;
  const parsedCommentedPosts = commentedPosts.split(",");
  console.log(parsedCommentedPosts);
  try {
    const job = async () => {
      try {
        const linkedinProfile = await scheduleJob("get_linkedin_profile", {
          linkedin_url: linkedinUrl,
          key: "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
        });
        console.log(linkedinProfile);
        const posts = linkedinProfile.recent_posts.filter(
          (post) =>
            parsedCommentedPosts.findIndex(
              (commentedPost) => commentedPost == post
            ) < 0
        );
        console.log(posts);
      } catch (error) {
        console.log("find-post-and-comment ERROR:", error);
      }
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/linkedin-login", async (req, res) => {
  const { email, password, proxyServer, proxyUsername, proxyPassword } =
    req.body;
  try {
    const { isLoggedIn, cookie, url, savedContext, error } = await scheduleJob(
      "login",
      {
        email: email,
        password: password,
        proxyServer: proxyServer,
        proxyUsername: proxyUsername,
        proxyPassword: proxyPassword,
      }
    );
    if (error) {
      return res.status(400).send(error);
    }
    if (isLoggedIn) {
      const profile = await scheduleJob("get_own_profile", {
        key: cookie.value,
      });
      const proxy = await Proxy.findOne({ key: cookie.value });
      if (!proxy) {
        await Proxy.create({
          server: proxyServer,
          username: proxyUsername,
          password: proxyPassword,
          key: cookie.value,
          linkedinUrl: profile.url,
        });
      } else {
        proxy.key = cookie.value;
        await proxy.save();
      }
      return res.status(200).send({ isLoggedIn, cookie });
    } else {
      return res.status(200).send({ isLoggedIn, url, savedContext });
    }
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/linkedin-security-code", async (req, res) => {
  const { code, url, savedContext, proxyServer, proxyUsername, proxyPassword } =
    req.body;
  try {
    const { cookie, error } = await scheduleJob("security_code", {
      code: code,
      url: url,
      savedContext: savedContext,
      proxyServer: proxyServer,
      proxyUsername: proxyUsername,
      proxyPassword: proxyPassword,
    });
    if (error) {
      return res.status(400).send(error);
    }
    const profile = await scheduleJob("get_own_profile", {
      key: cookie.value,
    });
    const proxy = await Proxy.findOne({ key: cookie.value });
    if (!proxy) {
      await Proxy.create({
        server: proxyServer,
        username: proxyUsername,
        password: proxyPassword,
        key: cookie.value,
        linkedinUrl: profile.url,
      });
    } else {
      proxy.key = cookie.value;
      await proxy.save();
    }
    return res.status(200).send({ cookie });
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

export default router;
