<template>
  <v-container>
      <v-row class="text-center">

        <v-col class="mb-0">
          <h1 class="display-1 font-weight-bold mb-3">DICOM Anonymization Pipeline</h1>

          <p class="subheading font-weight-regular">
            This is our DICOM Anonymization Pipeline for BME 528. 
            <br /> Users can query/retrieve DICOM files from 
            a PACS server based on patient ID
            <br /> Users can anonymize DICOM files and push the anonymized files into a PACS server
            <br /> Configuration options exist for modifying the level of anonymity 
            <!-- <br />Our codebase: 
            <a href="https://github.com/nikhilcusc/DICOMAnon" target="_blank"
              >Github repository</a
            > -->
          </p>
        </v-col>

      <v-col class="mb-0" cols="12">
        <h2 class="headline font-weight-bold mb-3">Codebase and Documentation</h2>

        <v-row justify="center">
          <a
            v-for="(next, i) in documentation"
            :key="i"
            :href="next.href"
            class="subheading mx-3"
            target="_blank"
          >
            {{ next.text }}
          </a>
        </v-row>
      </v-col>

        <v-col class= "mb-1" cols="12">
          <v-img
            :src="require('../assets/ProjectPipeline.png')"
            class="my-3"
            contain
            height="200"
          />
        </v-col>

    </v-row>

    <v-card width="900" class="mx-auto my-5">
      <v-alert type="error"
      v-model="fail_queryAlert"
      color="#B00020"
      dark
      dismissible
      >
      There was an error during query/retrieve. Please check your patient ID and try again!
      </v-alert>
      <v-alert type="success"
      v-model="success_queryAlert"
      dark
      dismissible
      >
      Query/Retrieve was successful! 
      </v-alert>
      <v-card-title>
        <h1 class="display-1">Query/Retrieve DICOM Files</h1>
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="patientId"
          label="Patient ID"
          prepend-icon="mdi-account"
          placeholder="12345"
          clearable
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          :loading="queryLoading"
          @click="postQuery"
        >
          Query
        </v-btn>
      </v-card-actions>
      <v-divider></v-divider>
    </v-card>

    <v-card width="900" class="mx-auto my-auto">
      <v-alert type="error"
      v-model="fail_anonAlert"
      color="#B00020"
      dark
      dismissible
      >
      There was an error during anonymization - please see console logs for details
      </v-alert>
      <v-alert type="success"
      v-model="success_anonAlert"
      dark
      dismissible
      >
      Anonymization and push were successful!
      </v-alert>
      <v-card-title>
        <h1 class="display-1">Anonymize & Push DICOM Files</h1>
      </v-card-title>
      <v-card-text>
        <v-file-input
          multiple
          label="Unanonymized DICOM files"
          v-model="inputDicom"
          hint=".dcm"
          placeholder="Example.dcm"
          clearable
          persistent-hint
          prepend-icon="mdi-file-search-outline"
          accept=".dcm"
          truncate-length="36"
        ></v-file-input>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          :loading="anonymizeLoading"
          @click="postAnonymize"
        >
          Anonymize & Push
        </v-btn>
      </v-card-actions>
      <v-divider></v-divider>
    </v-card>
  </v-container>
</template>
<script>
import axiosService from "@/service/axiosService";

export default {
  name: "HelloWorld",

  data: () => ({
    queryLoading: false,
    patientId: "",

    anonymizeLoading: false,
    inputDicom: null,

    fail_anonAlert: false,
    success_anonAlert: false,

    fail_queryAlert: false,
    success_queryAlert: false,

    documentation: [
      {
        text: "Github Repository",
        href: "https://github.com/nikhilcusc/DICOMAnon",
      },
    ],
  }),

  methods: {
    async postAnonymize() {
      //console.log(this.inputDicom);

      this.anonymizeLoading = true;
      if (this.inputDicom == null) {
        this.anonymizeLoading = false;
        console.log("Input Dicom file cannot be null");
        return;
      }

      var fileData = 0;
      var attachments = new FormData();
      this.inputDicom.forEach((file) => {
        attachments.append("inputDicomKey", file);
        fileData++;
      });
      //console.log("File Data below");

      let response = await axiosService.postAnonymizeData(attachments);
      //console.log(response);
      this.anonymizeLoading = false;
      if (response === "Done") {
        this.success_anonAlert = true;
        this.fail_anonAlert = false;
        console.log("Anonymization Successful");
      } else {
        this.success_anonAlert = false;
        this.fail_anonAlert = true;
        console.log("Anonymization Unsuccessful");
      }
    },

    async postQuery() {

      this.queryLoading = true;
      if (this.patientId == "") {
        this.queryLoading = false;
        console.log("Input Patient ID cannot be empty");
        return;
      }

      let response = await axiosService.postQueryData(this.patientId)
      console.log(response)
      this.queryLoading = false;

      if (response === "Done") {
        this.success_queryAlert = true;
        this.fail_queryAlert = false;
        console.log("Query Successful");
      } else {
        this.success_queryAlert = false;
        this.fail_queryAlert = true;
        console.log("Query Unsuccessful");
      }

    },
  },
};
</script>
