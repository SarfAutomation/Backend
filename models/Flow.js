import mongoose from "mongoose";

const FlowSchema = new mongoose.Schema({
  /**************************************************************************
   *                             Flow Information                           *
   **************************************************************************/
  account: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
  },
  sheetId: {
    type: String,  
  },
  sheetShared: {
    type: Boolean,
    default: false,
  },
  name: {
    type: String,
    required: true,
  },
  targetAudience: {
    type: String,
    required: true,
  },
  keyword: {
    type: String,
    required: true,
  },
  question: {
    type: String,
    required: true,
  },
  targetAmountResponse: {
    type: Number,
    default: 10,
  },
  lastPage: {
    type: Number,
    default: 0,
  },
  reachouts: [
    {
      name: {
        type: String,
        required: true,
      },
      linkedinUrl: {
        type: String,
      },
      response: {
        type: String,
      },
    },
  ],
});

export const Flow = mongoose.model("Flow", FlowSchema);
