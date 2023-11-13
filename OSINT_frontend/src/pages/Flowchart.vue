<script setup>
import { ref, onMounted } from "vue";
import { Icon } from "@iconify/vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useWindowSize } from "@vueuse/core";
import { VueFlow, useVueFlow, Position } from "@vue-flow/core";
/* these are necessary styles for vue flow */
import "@vue-flow/core/dist/style.css";
/* this contains the default theme, these are optional styles */
import "@vue-flow/core/dist/theme-default.css";

const router = useRouter();
const { _, height } = useWindowSize();

const root = ref([]);

const error = ref(false);

const elements = ref([
  {
    id: "root",
    type: "input",
    data: { nodeNum: 0 },
    label: "Main",
    position: { x: 10, y: Math.abs(height.value / 2 - 40) },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
    events: {
      click: (e) => {
        if (
          elements.value.find((el) => el.id === root.value[0].id) ||
          root.value.length === 0
        ) {
          elements.value = elements.value.filter(
            (el) => el.data.nodeNum <= e.node.data.nodeNum
          );
        } else {
          root.value.forEach((e) => {
            elements.value.push(e);
          });
        }
      },
    },
  },
]);

const getDataNodes = async (dataID, ID, nodeNum) => {
  try {
    const node = ref([]);

    await axios.get(`http://ec2-54-197-104-168.compute-1.amazonaws.com/folder/${dataID}/`).then((res) => {
      if (res.status === 200) {
        if (res.data.length === 0) {
          error.value = true;
          setTimeout((_) => (error.value = false), 5000);
        } else {
          res.data.forEach((e, i) => {
            if (e.parent_root === null && e.parent_folder === dataID) {
              node.value.push(
                {
                  id: `node${nodeNum + 1}-${i}`,
                  type: "default",
                  label: e.name,
                  data: { id: e.id, nodeNum: nodeNum + 1 },
                  position: {
                    x: Math.abs(250 * (nodeNum + 1)),
                    y:
                      res.data.length > 9
                        ? Math.abs(50 * i + 10)
                        : Math.abs((height.value / (res.data.length + 1)) * (i + 1) - 40),
                  },
                  sourcePosition: Position.Right,
                  targetPosition: Position.Left,
                  events: {
                    click: (e) => {
                      getDataNodes(
                        e.node.data.id,
                        e.node.id,
                        e.node.data.nodeNum
                      );
                    },
                  },
                },
                {
                  id: `${ID}/node${nodeNum + 1}-${i}`,
                  source: ID,
                  target: `node${nodeNum + 1}-${i}`,
                  data: { id: e.id, nodeNum: 1 },
                }
              );
            } else if (!e.parent_root && e.parent_folder === dataID) {
              node.value.push(
                {
                  id: `node${nodeNum + 1}-${i}`,
                  type: "output",
                  label: e.name,
                  data: {
                    id: e.id,
                    name: e.name,
                    nodeNum: nodeNum + 1,
                    image: e.image,
                    link: e.link,
                    steps: e.steps,
                  },
                  position: {
                    x: Math.abs(250 * (nodeNum + 1)),
                    y:
                      res.data.length > 9
                        ? Math.abs(50 * i + 10)
                        : Math.abs((height.value / (res.data.length + 1)) * (i + 1) - 40),
                  },
                  sourcePosition: Position.Right,
                  targetPosition: Position.Left,
                  events: {
                    click: (e) => {
                      window.open(router.resolve({ name: "child", query: e.node.data }).href, "_blank");
                      },
                  },
                },
                {
                  id: `${ID}/node${nodeNum + 1}-${i}`,
                  source: ID,
                  target: `node${nodeNum + 1}-${i}`,
                  data: { id: e.id, nodeNum: 1 },
                }
              );
            }
          });
        }
      } else {
        throw new Error(error);
      }
    });

    if (
      elements.value.find((el) => el.id === node.value[0]?.id) ||
      node.value.length === 0
    ) {
      elements.value = elements.value.filter(
        (el) => el.data.nodeNum <= nodeNum
      );
    } else {
      node.value.forEach((e) => {
        elements.value.push(e);
      });
    }
  } catch (error) {
    console.error(error.Message);
  }
};

const getDataNode = async (dataID, ID, nodeNum) => {
  try {
    const node = ref([]);

    await axios.get(`http://ec2-54-197-104-168.compute-1.amazonaws.com/root/${dataID}/`).then((res) => {
      if (res.status === 200) {
        if (res.data.length === 0) {
          error.value = true;
          setTimeout((_) => (error.value = false), 5000);
        } else {
          res.data.forEach((e, i) => {
            if (e.parent_root === dataID) {
              node.value.push(
                {
                  id: `node${nodeNum + 1}-${i}`,
                  type: "default",
                  label: e.name,
                  data: { id: e.id, nodeNum: nodeNum + 1 },
                  position: {
                    x: Math.abs(250 * (nodeNum + 1)),
                    y:
                      res.data.length > 9
                        ? Math.abs(50 * i + 10)
                        : Math.abs((height.value / (res.data.length + 1)) * (i + 1) - 40),
                  },
                  sourcePosition: Position.Right,
                  targetPosition: Position.Left,
                  events: {
                    click: (e) => {
                      getDataNodes(
                        e.node.data.id,
                        e.node.id,
                        e.node.data.nodeNum
                      );
                    },
                  },
                },
                {
                  id: `${ID}/node${nodeNum + 1}-${i}`,
                  source: ID,
                  target: `node${nodeNum + 1}-${i}`,
                  data: { id: e.id, nodeNum: 1 },
                }
              );
            }
          });
        }
      } else {
        throw new Error(error);
      }
    });

    if (
      elements.value.find((el) => el.id === node.value[0]?.id) ||
      node.value.length === 0
    ) {
      elements.value = elements.value.filter(
        (el) => el.data.nodeNum <= nodeNum
      );
    } else {
      node.value.forEach((e) => {
        elements.value.push(e);
      });
    }
  } catch (error) {
    console.error(error.Message);
  }
};

onMounted(_ => {
  try {
    axios.get("http://ec2-54-197-104-168.compute-1.amazonaws.com/root/").then((res) => {
      if (res.status === 200) {
        res.data.forEach((e, i) => {
          root.value.push(
            {
              id: `root-${i}`,
              type: "default",
              label: e.name,
              data: { id: e.id, nodeNum: 1 },
              position: {
                x: 250,
                y:
                  res.data.length > 9
                    ? Math.abs(50 * i + 10)
                    : Math.abs((height.value / (res.data.length + 1)) * (i + 1) - 40),
              },
              sourcePosition: Position.Right,
              targetPosition: Position.Left,
              events: {
                click: (e) => {
                  getDataNode(e.node.data.id, e.node.id, e.node.data.nodeNum);
                },
              },
            },
            {
              id: `root/root-${i}`,
              source: "root",
              target: `root-${i}`,
              data: { id: e.id, nodeNum: 1 },
            }
          );
        });
      } else {
        throw new Error(err);
      }
    });
  } catch (err) {
    console.error(err.Message);
  }
});

useVueFlow({
  defaultZoom: 1,
  preventScrolling: false,
  zoomOnScroll: false,
  zoomOnPinch: false,
  zoomOnDoubleClick: false,
  nodesDraggable: false,
  panOnDrag: false,
});
</script>

<template>
  <section>
    <VueFlow v-model="elements" />

    <div v-if="error" class="error">This folder is empty..</div>
  </section>
</template>

<style lang="scss" scoped>
section {
  width: 100vw;
  min-height: 100vh;
  display: flex;
}

.vue-flow {
  overflow: scroll;
  height: inherit;

  :deep(.vue-flow__node) {
    background: $first-color;
    border: 2px solid $third-color;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 1px;
    height: 40px;
    min-width: 100px;
    width: fit-content;
    padding-inline: 1rem;

    &.selected {
      border: 2px solid $third-color;
      box-shadow: none;
    }
  }

  :deep(.vue-flow__node-output) {
    background: $second-color;
  }

  :deep(.vue-flow__handle) {
    background: #000000;
    border: none;
    cursor: default;
  }

  :deep(.vue-flow__edge) {
    cursor: default;
  }

  :deep(.vue-flow__edge.selected > .vue-flow__edge-path),
  :deep(.vue-flow__edge-path) {
    stroke: $third-color;
    stroke-width: 2;
    cursor: default;
  }
}

.error {
  position: absolute;
  top: 2rem;
  inset-inline-start: 50%;
  transform: translateX(-50%);
  background: rgba($error-color, 0.5);
  padding: 1rem 2rem;
  border-radius: 12px;
}
</style>
