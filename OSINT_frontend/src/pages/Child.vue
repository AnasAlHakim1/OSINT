<script setup>
import { ref, onMounted } from "vue";
import { Icon } from "@iconify/vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
//axios.defaults.xsrfCookieName = "csrftoken"

const route = useRoute();
const router = useRouter();

const childData = ref({});
const showScripts = ref(false);

const file = ref(null);
const ProgressValue = ref("");
const progressResult = ref("");
const selectFile = ref(false);

const scriptData = ref(null);


onMounted(async (_) => {
  try {
    childData.value = {
      name: route.query.name,
      image: route.query.image,
      link: route.query.link,
      steps: route.query.steps,
      scripts: [],
    };

    await axios
      .get(`http://ec2-54-197-104-168.compute-1.amazonaws.com/api/child/${route.query.id}/`)
      .then((res) => {
        if (res.status === 200) {
          res.data.forEach((e) => {
            childData.value.scripts.push({
              id: e.id,
              name: e.name,
              script: e.python_script,
              // parent_child
            });
          });
        } else {
          throw new Error(error);
        }
      });

    if (childData.value.scripts.length > 0) {
      showScripts.value = true;
    } else {
      showScripts.value = false;
    }
  } catch (error) {
    console.error(error.Message);
  }
});

const getScript = async (ID) => {
  try {
      scriptData.value = {
      log_file: "",
      parent_script: "",
    };

    if (!file.value.files[0]) {
      selectFile.value = true;
    } else {
      await axios.get(`http://ec2-54-197-104-168.compute-1.amazonaws.com/api/script/${ID}/`).then((res) => {
        console.log(res);
        console.log("*********");
        if (res.status === 200) {
          const resultName = res.data.name;

          scriptData.value = {
            log_file: file.value.files[0],
            parent_script: res.data.id,
          };
          
          console.log(cookies.get('csrftoken'));
          console.log(scriptData.value);

          axios.post("http://ec2-54-197-104-168.compute-1.amazonaws.com/api/upload-log/", scriptData.value, {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            })
            .then((res) => {
              console.log("*************");
              console.log(res);
              if (res.status === 201) {
                const data = {
                  name: resultName,
                  result: res.data.result
                }
                window.open(router.resolve({ name: "script", query: data }).href, "_blank");
              } else {
                throw new Error(error);
              }
            });
        }
      });
    }
  } catch (error) {
    console.error(error.Message);
  }
};

const progressFile = _ => {
  let fileReader = new FileReader();

  if (file.value.files[0]) {
    fileReader.readAsDataURL(file.value.files[0]);

    fileReader.onload = (_) => {
      selectFile.value = false;
      progressResult.value = "Done!..";
    };
    fileReader.onerror = (_) => {
      progressResult.value = "Error!.. Please try agin.";
    };
    fileReader.onprogress = (data) => {
      if (data.lengthComputable) {
        ProgressValue.value =
          parseInt((data.loaded / data.total) * 100, 10) + "%";
      }
    };
  }
};

const closeScripts =  _ => {
  window.close();
};

const openImage = event => {
    window.open(event.target.src,'targetWindow', 'toolbar=no, location=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=768px, height=519px, top=25px, left=120px')
}
</script>

<template>
  <section v-if="childData">
    <Icon class="close" icon="ph:x-circle-duotone" @click="closeScripts" />

    <h1>{{ childData.name }}</h1>
    
    <div class="all">
      <div v-if="childData.image">
        <img
          :src="'http://ec2-54-197-104-168.compute-1.amazonaws.com' + childData.image"
          alt="Child Image"
          style="width: 100%;"
          @click="openImage($event)"
        />
      </div>

      <div>
        <div v-if="childData.steps">
          <h3>There is some steps :</h3>
          <pre>{{ childData.steps }}</pre>
        </div>

        <div v-if="childData.link">
          <h3>Visit the link for more information :</h3>
          <div>
            <a :href="childData.link" target="_blank">
              {{ childData.link }}
            </a>
          </div>
        </div>

        <form v-if="showScripts" @submit.prevent>
          <h3>Use scripts :</h3>
          <div>
            <label for="myfile">Select a file:</label>
            <input
              type="file"
              id="myFile"
              name="myFile"
              ref="file"
              @change="progressFile"
            />
            <div
              v-if="selectFile"
              class="selectError"
            >
              <span>Please select file...</span>
            </div>
            <div v-if="ProgressValue" style="margin-top: 0.5rem">
              <span>Progress: {{ ProgressValue }}</span>
              <span style="margin-inline-start: 1rem">{{ progressResult }}</span>
            </div>
            <div class="buttons-container">
              <button
                v-for="(scr, i) in childData.scripts"
                :key="i"
                @click="getScript(scr.id)"
              >
                {{ scr.name }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
section {
  padding-top: 2rem;
  padding-inline: 3rem;
  width: 100%;
  min-height: 100vh;
  background: rgba($first-color, 0.3);

  .all {
    margin-top: 2rem;
    display: inline-flex;
    width: 100%;
    align-items: center;
    justify-content: space-between;

    & > div {
      width: 50%;
    }
  }

  .close {
    width: 28px;
    height: 28px;
    position: absolute;
    top: 1rem;
    right: 1rem;
    color: $error-color;
    cursor: pointer;
  }

  h1 {
    font-size: 2rem;
    text-align: center;
  }

  h3 {
    margin-top: 1rem;

    & ~ div {
      padding-inline-start: 1rem;
    }

    & ~ pre {
      padding-inline-start: 1rem;
    }
  }

  form {
    label {
      margin-inline-end: 0.5rem;
    }

    input {
      cursor: pointer;
      
      &[type=file]::file-selector-button {
        border: 2px solid $third-color;
        padding: 0.2em 0.4em;
        border-radius: 0.2em;
        background-color: $second-color;
        cursor: pointer;
        transition: 0.2s;

        &:hover {
          background-color: rgba($second-color, 0.5);
        }
      }
    }

    .selectError {
      margin-top: 0.5rem;
      color: $error-color;
    }

    .buttons-container {
      margin-top: 0.75rem;
      display: flex;
      align-items: flex-start;
      flex-direction: column;
      gap: 0.5rem;

      button {
        padding: 0.5rem 1rem;
        background-color: $second-color;
        border: 2px solid $third-color;
        border-radius: 0.2em;
        font-size: 1rem;
        font-weight: bold;
        cursor: pointer;
        transition: 0.2s;

        &:hover {
          background-color: rgba($second-color, 0.5);
        }
      }
    }
  }
}
</style>
