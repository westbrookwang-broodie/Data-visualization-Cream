<template>
  <div id="word-cloud" style="">
  </div>
</template>

<script>
import * as d3 from 'd3';
import Papa from 'papaparse';
import * as cloud from 'd3-cloud';
const width = 1024
const height = 768
var sizeMap = [100, 60, 60, 50, 50, 40, 40, 30]
var data = [{
  word: '',
  count: 0
}]
var attackTypeMap = []
var targetTypeMap = []
var weaponTypeMap = []
var myWordCloud
var svg
var rot = 0
// var d = []
async function getData(filename){
  let this_ = this
  await d3.csv('src/data/' + filename, d=>({
    word: d.words,
    count: d.counts
  })).then(function (d){
    d = d.slice(0,100)
    data = d;
    console.log(data)
  })
}

function re() {
  var fill = d3.scaleOrdinal(d3.schemeTableau10);
  cloud().size([1000, 1000])
    .words(data, d => d.word)
    .padding(1)
    .rotate(() => ~~(Math.random() * 2) * 90 * ((rot++) % 2))
    //    .font("Impact")
    .text(d => d.word)
    .fontSize(function (d) {
      return d.count;
    })
    .on("end", draw)
    .start();


  function draw(words) {
    console.log(words)
    d3.pie()
    d3.select("#app").select("#word-cloud").append("svg")
      .attr("width", 1000)
      .attr("height", 1000)
      .append("g")
      .attr("transform", "translate(500,500)")
      .selectAll("text")
      .data(words)
      .enter().append("text")
      .style("font-size", function (d) {
        return d.count + "px";
      })
         .style("font-family", "KaiTi")
      .style("fill", function (d, i) {
        return fill(i);
      })
      .attr("text-anchor", "middle")
      .attr("transform", function (d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function (d) {
        return d.word;
      });
  }
}
// getData('words_流浪地球.csv')
// console.log(data)
function wordCloud(selector) {
  console.log(d3.select('div').select(selector))
  var svg = d3.select('div').select(selector).append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");


  var fill = d3.scaleOrdinal(d3.schemeTableau10);
  function draw(words) {
    var cloud = svg.selectAll(".cloud")
      .data(data, d => d.word)

    cloud.enter()
      .append("text")
      .attr("class", "cloud")
      .style("font-family", "Helvetica")
      .style("fill", (d, i) => fill(i))
      // .attr("text-anchor", "middle")
      .attr('font-size', d =>d.count/2)
      .text(d => d.word).attr("transform", function(d) {
      return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
    });

    // cloud
    //   .transition()
    //   .duration(10000)
    //   .attr('font-size', d => d.count + "px")
    //   // .attr('x', )
    //   .attr("transform", function(d) {
    //     console.log(d.x)      return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
    //   })
    //   .style("fill-opacity", 1);

    cloud.exit()
      .transition()
      .duration(500)
      .style('fill-opacity', 1e-6)
      .attr('font-size', 1)
      .remove();
  }

  return {
    update: function(data) {
      cloud().size([100,100])
        .words(data)
        .text(d=>d.word)
        .padding(5)
        .rotate(() => ~~(Math.random() * 2) * 90 * ((rot++) % 2))
        .font("Helvetica")
        .fontSize(d=>d.count)
        .on("end", draw)
        .start();
    }
  }
}
export default {
  name: "Cloud",
  data(){
    return{
      data: [{ text: 'dsadas',
        size: 40

      },
        { text: 'dsa342423das',
          size: 50

        },
        { text: 'd3214214adas',
          size: 60
        }
      ]
    }
  },
  methods:{
    init: function () {
      getData('words_流浪地球.csv')
    }
  },
  created() {
    // this.init()
  },
  async mounted() {
    this.init()
    setTimeout(() => {
      re()
      console.log(data)
    },500)




  }
}



</script>

<style scoped>

</style>
