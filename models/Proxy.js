import mongoose from "mongoose";

const ProxySchema = new mongoose.Schema({
  /**************************************************************************
   *                           Proxy Information                            *
   **************************************************************************/
  server: {
    type: String,
    required: true,
  },
  username: {
    type: String,
    required: true,
  },
  password: {
    type: String,
    required: true,
  },
  key: {
    type: String,
    required: true,
  },
});

export const Proxy = mongoose.model("Proxy", ProxySchema);
