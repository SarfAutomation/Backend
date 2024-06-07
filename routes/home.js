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
            ) < 0 && post.type.includes("posted")
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
            name: linkedinProfile.name,
            profile: linkedinUrl,
            post: posts[0],
            postContent: post,
            comment,
          }
        );
        console.log(comment);
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

router.post("/send-comment", async (req, res) => {
  const { postUrl, comment, key, name, profile } = req.body;
  console.log(postUrl, comment, key);
  try {
    const job = async () => {
      try {
        // await scheduleJob("comment_on_post", {
        //   post_url: postUrl,
        //   comment: comment,
        //   key: key,
        // });
        await axios.post(
          "https://hooks.zapier.com/hooks/catch/18369368/2y7kzna/",
          {
            postUrl,
            comment,
            name,
            profile,
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
        console.log(linkedinProfile);
        const response = await openai.chat.completions.create({
          messages: [
            {
              role: "system",
              content:
                "You are a connection request message writer, you will receive a JSON containing information about a linkedin profile and generate a very short human like message to connect with profile.",
            },
            {
              role: "user",
              content: `Here is the linkedin profile JSON: ${JSON.stringify(
                linkedinProfile
              )}, and here is what the user has commented on this person's post before ${comments}. return the message in the following JSON format: {"message": "Your connection request message here"}`,
            },
          ],
          model: "gpt-4o",
        });
        const completion = extractJSONFromString(
          response.choices[0].message.content
        );
        const message = completion.message;
        await axios.post(
          "https://hooks.zapier.com/hooks/catch/18369368/2ylmgl2/",
          {
            name: linkedinProfile.name,
            profile: { url: linkedinUrl, ...linkedinProfile },
            comments: comments,
            message: message,
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
          content: message,
          key: key,
        });
        await axios.post(
          "https://hooks.zapier.com/hooks/catch/18369368/2yjufiy/",
          {
            profile: linkedinUrl,
            message: message,
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
  const { searchUrl, key } = req.body;
  try {
    const job = async () => {
      try {
        // const result = await scheduleJob("search_sales_nav", {
        //   search_url: searchUrl,
        //   key: key,
        //   amount: 20,
        // });
        const result = [
          {
            name: "Prashant SK Shriyan",
            url: "https://www.linkedin.com/sales/lead/ACwAAB8kFDABtukMw5Neq1rihbvlbQoNE3kHLPQ,NAME_SEARCH,0enc?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
            isOpen: true,
          },
          {
            name: "Rima SBEI",
            url: "https://www.linkedin.com/sales/lead/ACwAACpmalIBW40jx343F8nUeOI9aO9WiyzYfdo,NAME_SEARCH,Qr40?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
            isOpen: false,
          },
          // {
          //   name: "Atis Mertens",
          //   url: "https://www.linkedin.com/sales/lead/ACwAAAtCduMBJu1NnSmXoFKxVD9u5U49HFwHySc,NAME_SEARCH,zFjY?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: true,
          // },
          // {
          //   name: "Nilesh Patil",
          //   url: "https://www.linkedin.com/sales/lead/ACwAAA13bqcB2QbUHjYNfh2ENVoQHeZh9JAzggM,NAME_SEARCH,Be8A?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: true,
          // },
          // {
          //   name: "Tudor Brad",
          //   url: "https://www.linkedin.com/sales/lead/ACwAAApV5eIBAU-iBSYEAuKep4COUE6xobo0Uxk,NAME_SEARCH,731Z?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Mariia Chesnova",
          //   url: "https://www.linkedin.com/sales/lead/ACwAADFFbggBnQVw8yCk3Fla0lThlbAFO2KImFg,NAME_SEARCH,F30G?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Matt Stager",
          //   url: "https://www.linkedin.com/sales/lead/ACwAAAAfc34BfyH0rXUaE8m7-wPX038-p9T6qs4,NAME_SEARCH,Crg4?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: true,
          // },
          // {
          //   name: "Supriya Chavan",
          //   url: "https://www.linkedin.com/sales/lead/ACwAADX05dsBWxGewX8kIit07RSrjoyIe4iJnos,NAME_SEARCH,Zgb3?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Marco Avila",
          //   url: "https://www.linkedin.com/sales/lead/ACwAAAp3zyQBNev9G-nc1vNHvyhTN8ZpRx20zbI,NAME_SEARCH,7zdx?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Rex Kumi",
          //   url: "https://www.linkedin.com/sales/lead/ACwAAAxTiqQBK4egPmIlSUHGtQMiTjzVUWSOnsY,NAME_SEARCH,_r2C?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Chandan Mishra",
          //   url: "https://www.linkedin.com/sales/lead/ACwAACiA7DwBZ1Rq_ro81XsrPOWi7U3OaWSBuJM,NAME_SEARCH,J_c-?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Ting Qiu",
          //   url: "https://www.linkedin.com/sales/lead/ACwAAApiP3AB5uqN2rm5jbAFW7NuhCewp4iEpfc,NAME_SEARCH,-9mK?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Aakash Kehar",
          //   url: "https://www.linkedin.com/sales/lead/ACwAAAQLKIkBaBG6Rql7Hswf5iM61StJqr0xfcU,NAME_SEARCH,TMXf?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: true,
          // },
          // {
          //   name: "Manuel Lopez Insausti",
          //   url: "https://www.linkedin.com/sales/lead/ACwAAAI0YVUBf89to_vRvWxf06-0529GDlH6gWA,NAME_SEARCH,w4Fm?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Max Shulgin",
          //   url: "https://www.linkedin.com/sales/lead/ACwAACRO7UUBtF7gHQ_4_u7Fvmljm8DyY2MpsVs,NAME_SEARCH,FZ9B?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Akshay M",
          //   url: "https://www.linkedin.com/sales/lead/ACwAADjXHY4BR5Rk07uGXysJmxpol58V9f6CyMc,NAME_SEARCH,5Tmi?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Vyacheslav(Slava) Meyerzon",
          //   url: "https://www.linkedin.com/sales/lead/ACwAABP3SdIBU3vdowMuqucIG7ROWiOdbHGiB3g,NAME_SEARCH,l0P6?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: true,
          // },
          // {
          //   name: "Clay Bennett",
          //   url: "https://www.linkedin.com/sales/lead/ACwAABMuWPcBYF806jCz8bqtXrq-TEjzMy_wZJ4,NAME_SEARCH,-tVA?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: true,
          // },
          // {
          //   name: "Tarek Kassem",
          //   url: "https://www.linkedin.com/sales/lead/ACwAABgCb28BdOAAY7hPt9JYU8aNwq1RSUhyZg0,NAME_SEARCH,PeS2?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: true,
          // },
          // {
          //   name: "Karya Boyraz",
          //   url: "https://www.linkedin.com/sales/lead/ACwAADQ8hKwBkrTtkOy8cV69DOmRlJJhS1iMfJg,NAME_SEARCH,Rcup?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: true,
          // },
          // {
          //   name: "Suranjan Rudra",
          //   url: "https://www.linkedin.com/sales/lead/ACwAACXCg8AByNBZD0zMdoL7i00yjVfmf3toGDk,NAME_SEARCH,Ze88?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Yaroslav Savka",
          //   url: "https://www.linkedin.com/sales/lead/ACwAACjzU0ABWLEiH7-uifs5j6CmMnzqlwO9UsA,NAME_SEARCH,2wJk?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Evangelos Papadopoulos",
          //   url: "https://www.linkedin.com/sales/lead/ACwAAAPBXE4BjG1qhL8zFV0R0QxaoqhVvxt2yXk,NAME_SEARCH,3JSE?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Shaik Wahab",
          //   url: "https://www.linkedin.com/sales/lead/ACwAAAdlUkgBVAeUnpKsZX5MIJqikcD4390mVWw,NAME_SEARCH,XLRx?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
          // {
          //   name: "Flemming Simonsen",
          //   url: "https://www.linkedin.com/sales/lead/ACwAAAEEI3IBmp8jHBArVc6xzUAu5HZZFEdQpxo,NAME_SEARCH,Kxdu?_ntb=iWPfJTyQQkSan6%2B6oe0FLQ%3D%3D",
          //   isOpen: false,
          // },
        ];
        await Promise.all(
          result.map(async (profile) => {
            try {
              console.log("bruh", profile)
              const linkedin = await scheduleJob("get_linkedin_url", {
                sales_nav_url: profile.url,
                key: key,
              });
              console.log("lmfao", profile)
              console.log(linkedin);
              await axios.post(
                "https://hooks.zapier.com/hooks/catch/18369368/2oyv0vs/",
                {
                  name: profile.name,
                  profile: linkedin.url,
                }
              );
            } catch (error) {
              console.log(error);
            }
          })
        );
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
      await proxy.save();
    }
    return res.status(200).send({ cookie });
  } catch (error) {
    console.log(error);
    return res.status(400).send("Something went wrong");
  }
});

export default router;
