import mongoose from "mongoose";

const ProxySchema = new mongoose.Schema({
  /**************************************************************************
   *                           Proxy Information                            *
   **************************************************************************/
  url: {
    type: String,
    required: true,
  },
  key: {
    type: String,
    required: true,
  },
});

export const Proxy = mongoose.model("Proxy", ProxySchema);
