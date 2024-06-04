function extractJSONFromString(str) {
    try {
      // Regular expression to match the JSON object
      const jsonString = str.match(/\{.*?\}/s);
      
      if (jsonString && jsonString[0]) {
        // Parse the JSON string to an object
        return JSON.parse(jsonString[0]);
      } else {
        throw new Error("No JSON object found in the string");
      }
    } catch (error) {
      console.error("Error parsing JSON from string:", error);
      return null;
    }
  }

  export { extractJSONFromString };