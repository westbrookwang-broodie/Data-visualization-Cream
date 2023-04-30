<template>
  <div>
    <div id="atlasMain"></div>
  </div>
</template>
<style scoped>
#atlasMain{
  width:2000px;
  height:2000px;
  margin-left: 300px;
}
</style>

<script>
import * as echarts from 'echarts';
import * as d3 from "d3";
import dataJson from './data.json'

export default {
  name: "cloud2"
}
</script>
