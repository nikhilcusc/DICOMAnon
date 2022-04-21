<template>
  <v-container>
      <v-row class="text-center">

        <v-col class="mb-4">
          <h1 class="display-1 font-weight-bold mb-3">DICOM Anonymization Pipeline</h1>

          <p class="subheading font-weight-regular">
            This is our DICOM Anonymization Pipeline for BME 528. 
            <br /> Users can query/retrieve DICOM files from 
            a PACS server based on patient ID
            <br /> Users can anonymize DICOM files and push the anonymized files into a PACS server
            <br /> Configuration options exist for modifying the level of anonymity 
            <br />Our codebase: 
            <a href="https://github.com/nikhilcusc/DICOMAnon" target="_blank"
              >Github repository</a
            >
          </p>
        </v-col>

        <v-col cols="12">
          <v-img
            :src="require('../assets/ProjectPipeline.png')"
            class="my-3"
            contain
            height="200"
          />
        </v-col>

      <v-col class="mb-5" cols="12">
        <h2 class="headline font-weight-bold mb-3">Documentation</h2>

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
    </v-row>
    <v-card width="900" class="mx-auto my-auto">
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
      <v-card-title>
        <h1 class="display-1">Anonymize DICOM Files</h1>
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
          Anonymize
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

    documentation: [
      {
        text: "Documentation Goes Here",
        href: "https://htmlpreview.github.io/?https://github.com/nikhilcusc/DICOMAnon/blob/main/docs/build/html/py-modindex.html",
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
        console.log("Anonymization Successful");
      } else {
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
        console.log("Query Successful");
      } else {
        console.log("Query Unsuccessful");
      }

    },
  },
};
</script>
