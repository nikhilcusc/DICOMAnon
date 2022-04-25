<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-0">
        <h1 class="display-1 font-weight-bold mb-3">
          DICOM Anonymization Pipeline
        </h1>

        <p class="subheading font-weight-regular">
          This is our DICOM Anonymization Pipeline for BME 528.
          <br />
          Users can query/retrieve DICOM files from a PACS server based on
          patient ID <br />
          Users can anonymize DICOM files and push the anonymized files into a
          PACS server <br />
          Users can configure the level of anonymity as soft, medium, or hard (hard being full anonymization) <br />
          Users can manually modify each DICOM tag to pick whether they will be part of the anonymization
        </p>
      </v-col>

      <v-col class="mb-0" cols="12">
        <h2 class="headline font-weight-bold mb-3">
          Codebase and Documentation
        </h2>

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

      <v-col class="mb-1" cols="12">
        <v-img
          :src="require('../assets/UpdatedProjectPipeline.png')"
          class="my-3"
          contain
          height="200"
        />
      </v-col>
    </v-row>

    <v-card width="900" class="mx-auto my-5">
      <v-alert
        type="error"
        v-model="fail_queryAlert"
        color="#B00020"
        dark
        dismissible
      >
        There was an error during query/retrieve. Please check your patient ID
        and try again!
      </v-alert>
      <v-alert type="success" v-model="success_queryAlert" dark dismissible>
        Query/Retrieve was successful! Please check the "ImageHeaders/DownloadedFiles" directory to view your files
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
        <v-btn color="primary" :loading="queryLoading" @click="postQuery">
          Query
        </v-btn>
      </v-card-actions>
      <v-divider></v-divider>
    </v-card>

    <v-card width="900" class="mx-auto my-auto">
      <v-alert
        type="error"
        v-model="fail_anonAlert"
        color="#B00020"
        dark
        dismissible
      >
        There was an error during anonymization - please see console logs for
        details
      </v-alert>
      <v-alert type="success" v-model="success_anonAlert" dark dismissible>
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

      <v-data-table
        v-model="selected"
        :headers="headers"
        :items="anonymizedTags"
        :items-per-page="5"
        item-key="name"
        class="elevation-1"
      >
        <template v-slot:item="{ item, isSelected, select }">
          <tr
            :class="isSelectedCompute(item.name) ? 'green' : ''"
            @click="toggle(isSelected, select, item.name, $event)"
          >
            <td class="d-flex align-center">
              {{ item.name }}
              <v-icon
                class="px-1"
                color="black"
                v-if="isSelectedCompute(item.name)"
                >mdi-check</v-icon
              >
            </td>
            <td>{{ item.group }}</td>
            <td>{{ item.element }}</td>
          </tr>
        </template>
      </v-data-table>

      <v-row>
        <v-col class="pa-5">
          <v-toolbar flat dense>
            <v-toolbar-title>
              <span class="subheading">Anonymization Severity</span>
            </v-toolbar-title>
          </v-toolbar>
          <v-slider
            @change="updateVueTable"
            :value="trackProgress"
            v-model="anonymization_severity"
            :tick-labels="anonymization_severityLabels"
            :max="2"
            step="1"
            ticks="always"
            tick-size="4"
          >
          </v-slider>
        </v-col>
      </v-row>
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
  name: "Dicom Anonymization",

  data: () => ({
    queryLoading: false,
    patientId: "",

    anonymizeLoading: false,
    inputDicom: null,

    fail_anonAlert: false,
    success_anonAlert: false,

    fail_queryAlert: false,
    success_queryAlert: false,

    anonymization_severity: 0,

    anonymization_severityLabels: ["Soft", "Medium", "Hard"],

    softGroupElementArray: [
      [0x10, 0x0010], // "Patient Name"
      [0x10, 0x0020], // "Patient ID"
      [0x08, 0x0050], // "Accession Number"
      [0x10, 0x0030], // "Patient's Birth Date"
      [0x10, 0x2155], // "Patient's Telecom Information"
      [0x10, 0x2154], // "Patient's Telephone Numbers"
      [0x10, 0x2297], // "Responsible Person"
    ],

    mediumGroupElementArray: [
      [0x10, 0x0010], // "Patient Name"
      [0x10, 0x0020], // "Patient ID"
      [0x08, 0x0050], // "Accession Number"
      [0x10, 0x0030], // "Patient's Birth Date"
      [0x10, 0x2155], // "Patient's Telecom Information"
      [0x10, 0x2154], // "Patient's Telephone Numbers"
      [0x10, 0x2297], // "Responsible Person"
      [0x10, 0x1005], // "Patient's Birth Name"
      [0x10, 0x2299], // "Responsible Organization"
      [0x10, 0x2180], // "Occupation"
      [0x08, 0x0090], // "Referring Physician's Name"
      [0x08, 0x0020], // "Study Date"
    ],

    fullNameArray: [
      "Patient Name",
      "Patient ID",
      "Patient's Birth Date",
      "Patient's Sex",
      "Other Patient IDs",
      "Other Patient Names",
      "Patient's Birth Name",
      "Military Rank",
      "Patient's Age",
      "Patient's Telephone Numbers",
      "Patient's Telecom Information",
      "Occupation",
      "Additional Patient's History",
      "Responsible Person",
      "Responsible Person Role",
      "Responsible Organization",
      "Patient Comments",
      "Study Date",
      "Study Time",
      "Accession Number",
      "Institution Name",
      "Institution Address",
      "Referring Physician's Name",
      "Referring Physician's Identification sequence",
      "Physician(s) of Record",
      "Physician(s) of Record Identification Sequence",
      "Name of Physician(s) Reading Study",
      "Physician Reading Study Identification Sequence",
    ],

    fullGroupElementArray: [
      [0x10, 0x0010], //"Patient Name"
      [0x10, 0x0020], //"Patient ID"
      [0x10, 0x0030], //"Patient's Birth Date"
      [0x10, 0x0040], //"Patient's Sex"
      [0x10, 0x1000], //"Other Patient IDs"
      [0x10, 0x1001], //"Other Patient Names"
      [0x10, 0x1005], //"Patient's Birth Name"
      [0x10, 0x1080], //"Military Rank"
      [0x10, 0x1010], //"Patient's Age"
      [0x10, 0x2154], //"Patient's Telephone Numbers"
      [0x10, 0x2155], //"Patient's Telecom Information"
      [0x10, 0x2180], //"Occupation"
      [0x10, 0x21b0], //"Additional Patient's History"
      [0x10, 0x2297], //"Responsible Person"
      [0x10, 0x2298], //"Responsible Person Role"
      [0x10, 0x2299], //"Responsible Organization"
      [0x10, 0x4000], //"Patient Comments"
      [0x08, 0x0020], //"Study Date"
      [0x08, 0x0030], //"Study Time"
      [0x08, 0x0050], //"Accession Number"
      [0x08, 0x0080], //"Institution Name"
      [0x08, 0x0081], //"Institution Address"
      [0x08, 0x0090], //"Referring Physician's Name"
      [0x08, 0x0096], //"Referring Physician's Identification sequence"
      [0x08, 0x1048], //"Physician(s) of Record"
      [0x08, 0x1049], //"Physician(s) of Record Identification Sequence"
      [0x08, 0x1060], //"Name of Physician(s) Reading Study"
      [0x08, 0x1062], //"Physician Reading Study Identification Sequence"
    ],

    fullGroupElementStringArray: [
      ["0x10", "0x0010"], //"Patient Name"
      ["0x10", "0x0020"], //"Patient ID"
      ["0x10", "0x0030"], //"Patient's Birth Date"
      ["0x10", "0x0040"], //"Patient's Sex"
      ["0x10", "0x1000"], //"Other Patient IDs"
      ["0x10", "0x1001"], //"Other Patient Names"
      ["0x10", "0x1005"], //"Patient's Birth Name"
      ["0x10", "0x1080"], //"Military Rank"
      ["0x10", "0x1010"], //"Patient's Age"
      ["0x10", "0x2154"], //"Patient's Telephone Numbers"
      ["0x10", "0x2155"], //"Patient's Telecom Information"
      ["0x10", "0x2180"], //"Occupation"
      ["0x10", "0x21B0"], //"Additional Patient's History"
      ["0x10", "0x2297"], //"Responsible Person"
      ["0x10", "0x2298"], //"Responsible Person Role"
      ["0x10", "0x2299"], //"Responsible Organization"
      ["0x10", "0x4000"], //"Patient Comments"
      ["0x08", "0x0020"], //"Study Date"
      ["0x08", "0x0030"], //"Study Time"
      ["0x08", "0x0050"], //"Accession Number"
      ["0x08", "0x0080"], //"Institution Name"
      ["0x08", "0x0081"], //"Institution Address"
      ["0x08", "0x0090"], //"Referring Physician's Name"
      ["0x08", "0x0096"], //"Referring Physician's Identification sequence"
      ["0x08", "0x1048"], //"Physician(s) of Record"
      ["0x08", "0x1049"], //"Physician(s) of Record Identification Sequence"
      ["0x08", "0x1060"], //"Name of Physician(s) Reading Study"
      ["0x08", "0x1062"], //"Physician Reading Study Identification Sequence"
    ],

    fullNameGroupElementArray: [
      ["Patient Name", 0x10, 0x0010],
      ["Patient ID", 0x10, 0x0020],
      ["Patient's Birth Date", 0x10, 0x0030],
      ["Patient's Sex", 0x10, 0x0040],
      ["Other Patient IDs", 0x10, 0x1000],
      ["Other Patient Names", 0x10, 0x1001],
      ["Patient's Birth Name", 0x10, 0x1005],
      ["Military Rank", 0x10, 0x1080],
      ["Patient's Age", 0x10, 0x1010],
      ["Patient's Telephone Numbers", 0x10, 0x2154],
      ["Patient's Telecom Information", 0x10, 0x2155],
      ["Occupation", 0x10, 0x2180],
      ["Additional Patient's History", 0x10, 0x21b0],
      ["Responsible Person", 0x10, 0x2297],
      ["Responsible Person Role", 0x10, 0x2298],
      ["Responsible Organization", 0x10, 0x2299],
      ["Patient Comments", 0x10, 0x4000],
      ["Study Date", 0x08, 0x0020],
      ["Study Time", 0x08, 0x0030],
      ["Accession Number", 0x08, 0x0050],
      ["Institution Name", 0x08, 0x0080],
      ["Institution Address", 0x08, 0x0081],
      ["Referring Physician's Name", 0x08, 0x0090],
      ["Referring Physician's Identification sequence", 0x08, 0x0096],
      ["Physician(s) of Record", 0x08, 0x1048],
      ["Physician(s) of Record Identification Sequence", 0x08, 0x1049],
      ["Name of Physician(s) Reading Study", 0x08, 0x1060],
      ["Physician Reading Study Identification Sequence", 0x08, 0x1062],
    ],

    groupElementArrayForAnonymization: [],

    selected: [],

    selectedRows: [],

    headers: [
      {
        text: "DICOM Tag Name",
        align: "left",
        sortable: false,
        value: "name",
      },
      { text: "Group Number", value: "group" },
      { text: "Element Number", value: "element" },
    ],

    anonymizedTags: [
      {
        id: 0,
        name: "Null",
        group: 0,
        element: 0,
      },
    ],

    documentation: [
      {
        text: "Github Repository",
        href: "https://github.com/nikhilcusc/DICOMAnon",
      },
    ],
  }),

  computed: {
    //////////////////////////////
    //// Function trackProgress()
    //// Tracks anonymization severity to slider
    //////////////////////////////
    trackProgress: function () {
      return this.anonymization_severity;
    },
  },

  methods: {
    //////////////////////////////
    //// Function isSelectedCompute()
    //// Updates rows in data table to highlight as green or neutral 
    //////////////////////////////
    isSelectedCompute(value) {
      return this.selectedRows.find((data) => data === value) ? true : false;
    },

    //////////////////////////////
    //// Function updateVueTable()
    //// Updates this.groupElementArrayForAnonymization with corresponding
    //// groupElementArray based on anonymization severity
    //////////////////////////////
    async updateVueTable() {

      this.selectedRows = [];
      // Assign anonymization list based on anonymization severity (0 is soft, 1 is medium, 2 is full/"hard")
      if (this.anonymization_severity === 0) {
        this.groupElementArrayForAnonymization = this.softGroupElementArray;
        this.softGroupElementArray.forEach((element) => {
          const id = element[1];
          var foundElement = this.fullNameGroupElementArray.find(
            (data) => data[2] === id
          );
          if (foundElement) {
            this.selectedRows.push(foundElement[0]);
          }
        });

      } else if (this.anonymization_severity === 1) {
        this.groupElementArrayForAnonymization = this.mediumGroupElementArray;
        this.mediumGroupElementArray.forEach((element) => {
          const id = element[1];
          var foundElement = this.fullNameGroupElementArray.find(
            (data) => data[2] === id
          );
          if (foundElement) {
            this.selectedRows.push(foundElement[0]);
          }
        });
      } else {
        this.selectedRows = this.fullNameGroupElementArray.map(
          (data) => data[0]
        );
        this.groupElementArrayForAnonymization = this.fullGroupElementArray;
      }
    },

    //////////////////////////////
    //// Function toggle()
    //// Updates this.groupElementArrayForAnonymization based on whether
    //// given tag group/element should be included
    //// Updates data table to visualize selected row
    //////////////////////////////
    async toggle(isSelected, select, tagName) {
      var tagFullIndex = this.fullNameArray.indexOf(tagName);
      var tagValue = this.fullGroupElementArray[tagFullIndex];

      var jsonAnonGroupElementArray = JSON.stringify(
        this.groupElementArrayForAnonymization
      );
      var jsonTagValue = JSON.stringify(tagValue);

      var jsonTagValueWithPrecedingComma = "," + jsonTagValue;
      var jsonTagValueWithAppendedComma = jsonTagValue + ",";

      var jsonTagAnonIndexWithAppendedComma = jsonAnonGroupElementArray.indexOf(
        jsonTagValueWithAppendedComma
      );
      var jsonTagAnonIndexWithPrecedingComma =
        jsonAnonGroupElementArray.indexOf(jsonTagValueWithPrecedingComma);

      // Replace tagValue with appended comma if it exists
      if (jsonTagAnonIndexWithAppendedComma != -1) {
        jsonTagValue = jsonTagValueWithAppendedComma;
      }

      // Replace tagValue with preceding comma if it exists
      if (jsonTagAnonIndexWithPrecedingComma != -1) {
        jsonTagValue = jsonTagValueWithPrecedingComma;
      }

      // Add or remove selected row from this.selectedRows (visualization of green)
      if (this.selectedRows.find((data) => data === tagName)) {
        this.selectedRows.splice(this.selectedRows.indexOf(tagName), 1);
        jsonAnonGroupElementArray = jsonAnonGroupElementArray.replace(
          jsonTagValue,
          ""
        );
        this.groupElementArrayForAnonymization = JSON.parse(
          jsonAnonGroupElementArray
        );
      } else {
        this.selectedRows.push(tagName);
        this.groupElementArrayForAnonymization.push(tagValue);
      }

      // Color row as green in data table
      select(!isSelected);
    },

    //////////////////////////////
    //// Function postAnonymize()
    //// Sends axios commands to update Python back-end with anonymization array
    //// Sends axios command to anonymize input DICOM file and push to PACS server
    //////////////////////////////
    async postAnonymize() {
      // Begin loading button
      this.anonymizeLoading = true;

      // Error out if input Dicom File is null
      if (this.inputDicom == null) {
        this.anonymizeLoading = false;
        this.success_anonAlert = false;
        this.fail_anonAlert = true;
        console.log("Input Dicom file cannot be null");
        return;
      }

      // Update python back-end with anonymization array
      // Error out if response is not "Done"
      let tableUpdate = await axiosService.updateAnonymizationTable(
        this.groupElementArrayForAnonymization
      );
      if (tableUpdate === "Done") {
        console.log("Python Update of tags to anonymize successful");
      } else {
        this.anonymizeLoading = false;
        this.success_anonAlert = false;
        this.fail_anonAlert = true;
        console.log("Python Update of tags to anonymize unsuccessful");
        return;
      }

      // Create form data 'attachments' based on input DICOM files
      var attachments = new FormData();
      this.inputDicom.forEach((file) => {
        attachments.append("inputDicomKey", file);
      });

      // Send input DICOM files to python back-end
      // End loading button
      // Error out if response is not "Done"
      let response = await axiosService.postAnonymizeData(attachments);
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

    //////////////////////////////
    //// Function postQuery()
    //// Posts to axiosService.postQueryData with patientId
    //// Sends query/retrieve request based on patientId
    //// Visualizes success or failure alert based on response
    //////////////////////////////
    async postQuery() {
      this.queryLoading = true;
      if (this.patientId == "") {
        this.queryLoading = false;
        console.log("Input Patient ID cannot be empty");
        return;
      }

      let response = await axiosService.postQueryData(this.patientId);

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

  //////////////////////////////
  //// Set up UI environment before mounting
  //////////////////////////////
  beforeMount() {
    // Populate table by iterating through full list of DICOM name, group, and elements
    for (let step = 0; step < this.fullGroupElementArray.length; step++) {
      if (step === 0) {
        this.anonymizedTags[0] = {
          id: step,
          name: this.fullNameArray[step],
          group: this.fullGroupElementStringArray[step][0],
          element: this.fullGroupElementStringArray[step][1],
        };
      } else {
        this.anonymizedTags.push({
          id: step,
          name: this.fullNameArray[step],
          group: this.fullGroupElementStringArray[step][0],
          element: this.fullGroupElementStringArray[step][1],
        });
      }
    }

    // Default the anonymization group to "soft"
    this.groupElementArrayForAnonymization = this.softGroupElementArray;
    this.updateVueTable();
  },
};
</script>
