import axios from "axios";
axios.defaults.headers.common["Content-Type"] = "multipart/form-data";
axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
axios.defaults.headers.common["Access-Control-Allow-Credentials"] = "true";

const axiosService = {
  /**
   * Anonymize data
   *
   * @param {object} attachments Input .dcm file
   *
   * @returns 'Done' if Anonymization and push were successful
   */
  postAnonymizeData: async function (attachments) {
    try {
      var response = await axios.post(
        "http://127.0.0.1:5000/" + `anonymize`,
        attachments,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            "Access-Control-Allow-Origin": "*",
          },
        }
      );
      return response.data;
    } catch (error) {
      console.log(error);
      return error;
    }
  },

  /**
   * Anonymize data
   *
   * @param {object} anonymizationArray Array of DICOM Group/Elements to anonymize
   *
   * @returns 'Done' if update to python back-end was successful
   */
  updateAnonymizationTable: async function (anonymizationArray) {
    try {
      var response = await axios.post(
        "http://127.0.0.1:5000/" + `updateAnonymizationTable`,
        { anonymizationArray: anonymizationArray }
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
