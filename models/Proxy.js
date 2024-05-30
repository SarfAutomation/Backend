import mongoose from "mongoose";

const ProxySchema = new mongoose.Schema({
  /**************************************************************************
   *                           Proxy Information                            *
   **************************************************************************/
  server: {
    type: String,
    default: "",
  },
  username: {
    type: String,
    default: "",
  },
  password: {
    type: String,
    default: "",
  },
  key: {
    type: String,
    default: "",
  },
  linkedinUrl: {
    type: String,
    required: true,
  }
});

export const Proxy = mongoose.model("Proxy", ProxySchema);
