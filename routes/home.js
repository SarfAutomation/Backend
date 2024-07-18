import express from "express";
import dotenv from "dotenv";
import { Proxy } from "../models/Proxy.js";
import { scheduleJob } from "../utils/JobQueue.js";
import axios from "axios";
import OpenAI from "openai";
import { extractJSONFromString } from "../utils/extractJson.js";
import { content } from "googleapis/build/src/apis/content/index.js";

dotenv.config();
const router = express.Router();
const openai = new OpenAI();

const LUDI_KEY =
  "AQEDAUcY98sE2bvuAAABkKQ4wzUAAAGQyEVHNVYAQpWvg8q8daxCTaGuM1TCjEKUDGVDzhRHFWHYS0gkSz-vugZApv3vOE8ga7svn4_eHr27uqpDOYxCZAoT3TjQ7A03XxpnlvyQIs2Lbd8bOqyXwG0y";

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
  const { key, timeOffset } = req.body;
  try {
    const job = async () => {
      try {
        const data = await scheduleJob("get_recent_connections", {
          key: key,
          time_offset: parseInt(timeOffset),
        });
        await Promise.all(
          data.map(async (linkedinUrl) => {
            // let salesNavUrl;
            // try {
            //   salesNavUrl = await scheduleJob("get_sales_nav_url", {
            //     linkedin_url: linkedinUrl,
            //     list: "dream100",
            //     key: key,
            //     list: key.slice(0, 75),
            //     key: LUDI_KEY
            //   });
            // } catch (error) {
            //   return;
            // }
            // console.log(salesNavUrl);
            // if (salesNavUrl.name && salesNavUrl.url) {
            //   await axios.post(
            //     "https://hooks.zapier.com/hooks/catch/18369368/2ois7ax/",
            //     {
            //       salesNavUrl,
            //       key,
            //     }
            //   );
            // }
            const profile = await scheduleJob("get_linkedin_profile", {
              linkedin_url: linkedinUrl,
              key: key,
            });
            await axios.post(
              "https://hooks.zapier.com/hooks/catch/18369368/2ois7ax/",
              {
                name: profile.name,
                profile: linkedinUrl,
                key,
              }
            );
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

router.post("/generate-comment", async (req, res) => {
  const { linkedinUrl, commentedPosts, key } = req.body;
  const parsedCommentedPosts = commentedPosts.split(",");
  console.log(parsedCommentedPosts);
  try {
    const job = async () => {
      try {
        const linkedinProfile = await scheduleJob("get_linkedin_profile", {
          linkedin_url: linkedinUrl,
          key: key,
        });
        console.log(linkedinProfile);
        const posts = linkedinProfile.recent_posts.filter(
          (post) =>
            parsedCommentedPosts.findIndex(
              (commentedPost) => commentedPost == post.url
            ) < 0 &&
            post.type.includes("posted") &&
            !post.type.includes("reposted")
        );
        if (!posts.length) {
          return;
        }
        let post = await scheduleJob("get_post", {
          post_url: posts[0].url,
          key: key,
        });
        post = { type: posts[0].type, ...post };
        const response = await openai.chat.completions.create({
          messages: [
            {
              role: "system",
              content:
                "You are a comment writer, you will receive a JSON containing information about a linkedin post and generate a short human like comment for this post.",
            },
            {
              role: "user",
              content: `Here is the post JSON: ${JSON.stringify(
                post
              )}, return the comment in the following JSON format: {"comment": "Your comment here"}`,
            },
          ],
          model: "gpt-4o",
        });
        const completion = extractJSONFromString(
          response.choices[0].message.content
        );
        const comment = completion.comment;
        await axios.post(
          "https://hooks.zapier.com/hooks/catch/18369368/3j74gm9/",
          {
            key: key,
            name: linkedinProfile.name,
            profile: linkedinUrl,
            post: posts[0],
            postContent: post,
            comment,
          }
        );
        console.log(comment);
      } catch (error) {
        console.log("generate-comment ERROR:", error);
      }
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/send-comment", async (req, res) => {
  const { postUrl, comment, key, name, profile } = req.body;
  console.log(postUrl, comment, key);
  try {
    const job = async () => {
      try {
        await scheduleJob("comment_on_post", {
          post_url: postUrl,
          comment: comment ? comment : "[empty message]",
          key: key,
        });
        await axios.post(
          "https://hooks.zapier.com/hooks/catch/18369368/2y7kzna/",
          {
            postUrl,
            comment,
            name,
            profile,
            key,
          }
        );
      } catch (error) {
        console.log("send-comment ERROR:", error);
      }
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/generate-cr-message", async (req, res) => {
  const { linkedinUrl, comments, key } = req.body;
  console.log(linkedinUrl, key);
  try {
    const job = async () => {
      try {
        const linkedinProfile = await scheduleJob("get_linkedin_profile", {
          linkedin_url: linkedinUrl,
          key: key,
        });
        // console.log(linkedinProfile);
        // const response = await openai.chat.completions.create({
        //   messages: [
        //     {
        //       role: "system",
        //       content:
        //         "You are a connection request message writer, you will receive a JSON containing information about a linkedin profile and generate a very short human like message to connect with profile.",
        //     },
        //     {
        //       role: "user",
        //       content: `Here is the linkedin profile JSON: ${JSON.stringify(
        //         linkedinProfile
        //       )}, and here is what the user has commented on this person's post before ${comments}. return the message in the following JSON format: {"message": "Your connection request message here"}`,
        //     },
        //   ],
        //   model: "gpt-4o",
        // });
        // const completion = extractJSONFromString(
        //   response.choices[0].message.content
        // );
        // const message = completion.message;
        const message = "";
        await axios.post(
          "https://hooks.zapier.com/hooks/catch/18369368/2ylmgl2/",
          {
            name: linkedinProfile.name,
            profile: { url: linkedinUrl, ...linkedinProfile },
            comments: comments,
            message: message,
            key: key,
          }
        );
        console.log(message);
      } catch (error) {
        console.log("send-comment ERROR:", error);
      }
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/send-cr-message", async (req, res) => {
  const { linkedinUrl, message, key } = req.body;
  try {
    const job = async () => {
      try {
        await scheduleJob("request_connect_linkedin", {
          linkedin_url: linkedinUrl,
          content: message ? message : "[empty message]",
          key: key,
        });
        await axios.post(
          "https://hooks.zapier.com/hooks/catch/18369368/2yjufiy/",
          {
            profile: linkedinUrl,
            message: message,
            key: key,
          }
        );
      } catch (error) {
        console.log("send-comment ERROR:", error);
      }
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/add-from-sales-nav-search", async (req, res) => {
  const { searchUrl, key, amount } = req.body;
  try {
    const job = async () => {
      try {
        const profiles = await scheduleJob("search_sales_nav", {
          search_url: searchUrl,
          key: LUDI_KEY,
          // key: key,
          amount: amount,
        });
        for (const profile of profiles) {
          try {
            const { name, url } = profile;
            const linkedin = await scheduleJob("get_linkedin_url", {
              sales_nav_url: url,
              key: LUDI_KEY,
              // key: key,
            });
            await axios.post(
              "https://hooks.zapier.com/hooks/catch/18369368/2oyv0vs/",
              {
                name: name,
                profile: linkedin.url,
                key: key,
              }
            );
            await scheduleJob("add_sales_nav_list", {
              profile_link: url,
              list: key.slice(0, 75),
              key: LUDI_KEY,
              // list: "dream100",
              // key: key,
            });
          } catch (error) {
            console.log(error);
          }
        }
      } catch (error) {
        console.log("add-from-sales-nav-search ERROR:", error);
      }
    };
    job();
    return res.status(200).send("Started");
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

router.post("/get-notifications", async (req, res) => {
  const { key, timeOffset } = req.body;
  try {
    const job = async () => {
      try {
        const notifications = await scheduleJob("get_notifications", {
          key: key,
          time_offset: parseInt(timeOffset),
        });
        const names = new Set();
        const uniqueNameNotification = notifications.filter((notification) => {
          if (!names.has(notification.name)) {
            names.add(notification.name);
            return true;
          }
          return false;
        });
        await axios.post(
          "https://hooks.zapier.com/hooks/catch/18369368/2o9ullr/",
          {
            notifications: uniqueNameNotification,
            key: key,
          }
        );
      } catch (error) {
        console.log("get-notifications ERROR:", error);
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
      const proxy = await Proxy.findOne({ linkedinUrl: profile.url });
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
        proxy.server = proxyServer;
        proxy.username = proxyUsername;
        proxy.password = proxyPassword;
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
    // const profile = await scheduleJob("get_own_profile", {
    //   key: cookie.value,
    // });
    const proxy = await Proxy.findOne({ linkedinUrl: profile.url });
    if (!proxy) {
      await Proxy.create({
        server: proxyServer,
        username: proxyUsername,
        password: proxyPassword,
        key: cookie.value,
        // linkedinUrl: profile.url,
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
