import axios from "axios";
axios.defaults.headers.common["Content-Type"] = "multipart/form-data"
axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
axios.defaults.headers.common["Access-Control-Allow-Credentials"] = "true";

const axiosService = {
  /**
   * Anonymize data
   *
   * @param {object} attachments Input .dcm file
   *
   * @returns 'Done' if Anonymization was successful
   */
  postAnonymizeData: async function (attachments) {

    //console.log("Axios Service attachment below")
    //console.log(attachments)

    try {
      var response = await axios.post(
        "http://127.0.0.1:5000/" + `anonymize`,
        attachments,
        { headers: { "Content-Type": "multipart/form-data", "Access-Control-Allow-Origin": "*"} }
      );
      return response.data;
    } catch (error) {
      console.log(error);
      return error;
    }
  },

  /**
   * Query/Receive DICOM data based on patient ID
   *
   * @param {integer} Patient ID 
   *
   * @returns 'Done' if Query was successful
   */
     postQueryData: async function (patientId) {

      console.log("Axios Service attachment below")
      console.log(patientId)
  
      try {
        var response = await axios.post(
          "http://127.0.0.1:5000/" + `query/` + patientId
        );
        return response.data;
      } catch (error) {
        console.log(error);
        return error;
      }
    },
};

export default axiosService;
