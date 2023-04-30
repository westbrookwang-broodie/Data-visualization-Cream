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
  name: "graph",
  data() {
    return {
      data: []
    }

  },
  created() {
      this.$nextTick(function () {
      this.initChart()
    })
  },
  methods: {
    initChart() {
      var chartDom = document.getElementById('atlasMain');
      var myChart = echarts.init(chartDom);
      var option;
      function ls (graph) {
        myChart.hideLoading();
        graph.nodes.forEach(function (node) {
          node.label = {
            show: node.symbolSize > 30
          };
        });
        option = {
          title: {
            text: 'Les Miserables',
            subtext: 'Default layout',
            top: 'bottom',
            left: 'right'
          },
          tooltip: {},
          legend: [
            {
              // selectedMode: 'single',
              data: graph.categories.map(function (a) {
                return a.name;
              })
            }
          ],
          animationDuration: 1500,
          animationEasingUpdate: 'quinticInOut',
          series: [
            {
              name: 'Les Miserables',
              type: 'graph',
              layout: 'none',
              data: graph.nodes,
              links: graph.links,
              categories: graph.categories,
              roam: true,
              label: {
                position: 'right',
                formatter: '{b}'
              },
              lineStyle: {
                color: 'source',
                curveness: 0.3
              },
              emphasis: {
                focus: 'adjacency',
                lineStyle: {
                  width: 10
                }
              }
            }
          ]
        };
        myChart.setOption(option);
      };
      ls(dataJson)
    option && myChart.setOption(option);

    }
  }
}
</script>
