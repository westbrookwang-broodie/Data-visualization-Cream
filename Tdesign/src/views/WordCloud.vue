<template>
  <div>
  <div id="word-cloud" style= "display: flex">
    <div style="width: 500px">
    <h1 aria-label="电影" style="font-size: 50px; font-family: KaiTi">电影</h1>
    <div class="letter svelte-1icc79m"><p class="svelte-1icc79m">
<!--      <span class="sr-only">电影</span> -->
      <span class="tagline is-del">是镜头语言<del>能表达一些平时不敢表达的东西.</del><ins class="svelte-1icc79m is-visible"></ins></span>
      <span class="popular svelte-1icc79m is-visible">你肯定看过
    		<a onclick="generate('霸王别姬')">
    			<span>霸王别姬</span></a>
				<img src="src/assets/img_6.png" alt="story thumbnail">它探讨了情感、性别和文化等多重主题。另外，
    		<a onclick="generate('我不是药神')">
    			<span>我不是药神</span></a>
				<img src="src/assets/img_1.png" alt="story thumbnail"> 通过一个药品销售员的故事，揭示了中国医疗体系中的现实问题。
    		<a onclick="generate('少年的你')">
    			<span>少年的你</span></a>
				<img src="src/assets/img_2.png" alt="story thumbnail">以青春成长为主线，深刻反映了当代社会中的青少年问题。
    </span> <span class="personal svelte-1icc79m is-visible">黑色幽默的经典之作
    		<a onclick="generate('让子弹飞')">
    			<span>让子弹飞</span></a>
				<img src="src/assets/img_3.png" alt="story thumbnail">获得了广泛赞誉。
    		<a onclick="generate('西虹市首富')">
    			<span>西虹市首富</span></a>
				<img src="src/assets/img_4.png" alt="story thumbnail">是一部现实主义喜剧，通过对“富豪梦”的嘲讽，深刻探讨了人性的弱点。
    		<a onclick="generate('绿皮书')">
    			<span>绿皮书</span></a>
				<img src="src/assets/img_2.png" alt="story thumbnail">是一部温情感人的励志片，描绘了一个黑人钢琴家和他的意大利裔司机之间的不凡旅程。</span>
      <span class="welcome svelte-1icc79m is-visible">这些优秀的电影作品，在各自领域均有突出表现，值得观众们品味、欣赏和探索。</span></p></div>
<!--    <t-select-->
<!--      autoWidth-->
<!--      borderless-->
<!--      size="large" @change="generate" placeholder="流浪地球">-->
<!--      <t-option key="少年的你" label="少年的你" value="少年的你" />-->
<!--      <t-option key="我不是药神" value="我不是药神">我不是药神</t-option>-->
<!--      <t-option key="流浪地球" label="流浪地球" value="流浪地球" />-->
<!--      <t-option key="绿皮书" label="绿皮书" value="绿皮书" />-->
<!--      <t-option key="西虹市首富" label="西虹市首富" value="西虹市首富" />-->
<!--      <t-option key="让子弹飞" label="让子弹飞" value="让子弹飞" />-->
<!--    </t-select>-->
    </div>
    <div id="world-cloud-graph" style="margin-top: 20%"></div>
  </div>
    <div style="margin-top: 20px">
      <h2 style="font-weight: bold; left: 25%; font-style: italic">情感分析热图</h2>
      <HeapMap></HeapMap>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
// import Papa from 'papaparse';
import * as cloud from 'd3-cloud';
import { select } from 'd3'
import HeapMap from "@/views/HeatMap.vue";
const width = 600
const height = 400
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
var graph
var cloud1
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
async function generate(item){
  await getData('words_'+item.toString()+'.csv')
  myWordCloud.update(data)
}

  window.generate= async function (item) {
    await getData('words_'+item.toString()+'.csv')
    myWordCloud.update(data)
  }
function re() {
  var fill = d3.scaleOrdinal(d3.schemeTableau10);


  // d3.pie()
  var svg = d3.select("#app").select("#word-cloud").select("#world-cloud-graph").append("svg")
    .attr("width", 400)
    .attr("height", 400)
    .append("g")
    .attr("transform", "translate(200,200)")


  graph = svg.selectAll("text")
  cloud1 = graph.data(data);
  function draw(words) {
    console.log(words)
    graph = svg.selectAll("text")
    cloud1 = graph.data(words)
    cloud1.enter().append("text")
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

    cloud1
      .transition()
      .duration(100)
      .attr('font-size', d => d.count)
      .attr("transform", function(d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function (d) {
        return d.word;
      })
      .style("fill-opacity", 1);

    // cloud1.
    // exit()
    //   .transition()
    //   .duration(500)
    //   .style('fill-opacity', 1e-6)
    //   .attr('font-size', 1)
    //   .remove();
  }
  cloud().size([400, 400])
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
  return {
    update: function(data) {
      // cloud.clear()
      cloud().size([400,400])
        .words(data)
        .text((d)=>d.word)
        .padding(1)
        .rotate(() => ~~(Math.random() * 2) * 90 * ((rot++) % 2))
        .fontSize((d)=>d.count)
        .on("end", draw)
        .start();

    }
  }
}
export default {
  name: "Cloud",
  components: {HeapMap},
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
      getData('words_霸王别姬.csv')
    },
    generate: async function (item){
      await getData('words_'+item.toString()+'.csv')
      myWordCloud.update(data)
    },
  },
  created() {
    // this.init()
  },
  async mounted() {
    this.init()
    setTimeout(() => {
      myWordCloud =re()
      console.log(myWordCloud)
    },500)




  }
}



</script>

<style scoped>

.hero-text h1 {
  margin: 0;
}

.hero-text p {
  font-weight: var(--font-weight-thin);
  font-size: var(--font-size-large)
}
section.svelte-1icc79m.svelte-1icc79m {
  margin-bottom: 4em
}

.letter.svelte-1icc79m.svelte-1icc79m {
  min-height: 60vh
}

.letter.svelte-1icc79m p.svelte-1icc79m {
  margin: 0
}

.letter del {
  text-decoration: none;
  background-image: -webkit-gradient(linear,left top,left bottom,from(currentColor),to(currentColor));
  background-image: -o-linear-gradient(currentColor,currentColor);
  background-image: linear-gradient(currentColor,currentColor);
  background-repeat: no-repeat;
  background-size: 0 .1em;
  background-position: 0 50%;
  -webkit-transition: background-size 1s ease-in;
  -o-transition: background-size 1s ease-in;
  transition: background-size 1s ease-in
}

.letter .is-del del {
  background-size: 100% .1em
}

.letter del:before {
  content: " [deletion start] "
}

.letter del:after {
  content: " [deletion end] "
}

ins.svelte-1icc79m.svelte-1icc79m {
  text-decoration: none;
  opacity: 0;
  -webkit-transition: opacity 1s ease-in 1s;
  -o-transition: opacity 1s ease-in 1s;
  transition: opacity 1s ease-in 1s
}

ins.is-visible.svelte-1icc79m.svelte-1icc79m {
  opacity: 1
}

.popular.svelte-1icc79m.svelte-1icc79m {
  opacity: 0;
  -webkit-transition: opacity 1s ease-in 3s;
  -o-transition: opacity 1s ease-in 3s;
  transition: opacity 1s ease-in 3s
}

.popular.is-visible.svelte-1icc79m.svelte-1icc79m {
  opacity: 1
}

.personal.svelte-1icc79m.svelte-1icc79m {
  opacity: 0;
  -webkit-transition: opacity 1s ease-in 4s;
  -o-transition: opacity 1s ease-in 4s;
  transition: opacity 1s ease-in 4s
}

.personal.is-visible.svelte-1icc79m.svelte-1icc79m {
  opacity: 1
}

.welcome.svelte-1icc79m.svelte-1icc79m {
  opacity: 0;
  -webkit-transition: opacity 1s ease-in 5s;
  -o-transition: opacity 1s ease-in 5s;
  transition: opacity 1s ease-in 5s
}

.welcome.is-visible.svelte-1icc79m.svelte-1icc79m {
  opacity: 1
}

.letter img {
  display: inline-block;
  width: 2em;
  -webkit-transform: translate(0,25%);
  transform: translateY(25%);
  outline: 1px solid var(--color-off-black)
}

.popular a+img,.personal a+img {
  -webkit-transition: outline var(--transition-fast) var(--transition-ease),-webkit-transform var(--transition-fast) var(--transition-ease);
  transition: outline var(--transition-fast) var(--transition-ease),-webkit-transform var(--transition-fast) var(--transition-ease);
  -o-transition: transform var(--transition-fast) var(--transition-ease),outline var(--transition-fast) var(--transition-ease);
  transition: transform var(--transition-fast) var(--transition-ease),outline var(--transition-fast) var(--transition-ease);
  transition: transform var(--transition-fast) var(--transition-ease),outline var(--transition-fast) var(--transition-ease),-webkit-transform var(--transition-fast) var(--transition-ease)
}

.popular a:hover+img,.personal a:hover+img {
  -webkit-transform: scale(1.2,1.2) translate(0,15%);
  transform: scale(1.2) translateY(15%);
  outline: 2px solid var(--color-off-black)
}
:root {
  --color-black: #1a1a1a;
  --color-off-black: #282828;
  --color-gray-dark: #6a6a6a;
  --color-gray-medium: #949494;
  --color-gray-light: #c9c9c9;
  --color-off-white: #f0f0f0;
  --color-white: #ffffff;
  --color-purple: #a973ff
}

html {
  line-height: 1.15;
  -webkit-text-size-adjust: 100%
}

body {
  margin: 0
}

main {
  display: block
}

/*h1 {*/
/*  font-size: 2em;*/
/*  margin: .67em 0*/
/*}*/

hr {
  box-sizing: content-box;
  height: 0;
  overflow: visible
}

pre {
  font-family: monospace,monospace;
  font-size: 1em
}

a {
  background-color: transparent
}

abbr[title] {
  border-bottom: none;
  text-decoration: underline;
  text-decoration: underline dotted
}

b,strong {
  font-weight: bolder
}

code,kbd,samp {
  font-family: monospace,monospace;
  font-size: 1em
}

small {
  font-size: 80%
}

sub,sup {
  font-size: 75%;
  line-height: 0;
  position: relative;
  vertical-align: baseline
}

sub {
  bottom: -.25em
}

sup {
  top: -.5em
}

img {
  border-style: none
}

button,input,optgroup,select,textarea {
  font-family: inherit;
  font-size: 100%;
  line-height: 1.15;
  margin: 0
}

button,input {
  overflow: visible
}

button,select {
  text-transform: none
}

button,[type=button],[type=reset],[type=submit] {
  -webkit-appearance: button
}

button::-moz-focus-inner,[type=button]::-moz-focus-inner,[type=reset]::-moz-focus-inner,[type=submit]::-moz-focus-inner {
  border-style: none;
  padding: 0
}

button:-moz-focusring,[type=button]:-moz-focusring,[type=reset]:-moz-focusring,[type=submit]:-moz-focusring {
  outline: 1px dotted ButtonText
}

fieldset {
  padding: .35em .75em .625em
}

legend {
  box-sizing: border-box;
  color: inherit;
  display: table;
  max-width: 100%;
  padding: 0;
  white-space: normal
}

progress {
  vertical-align: baseline
}

textarea {
  overflow: auto
}

[type=checkbox],[type=radio] {
  box-sizing: border-box;
  padding: 0
}

[type=number]::-webkit-inner-spin-button,[type=number]::-webkit-outer-spin-button {
  height: auto
}

[type=search] {
  -webkit-appearance: textfield;
  outline-offset: -2px
}

[type=search]::-webkit-search-decoration {
  -webkit-appearance: none
}

::-webkit-file-upload-button {
  -webkit-appearance: button;
  font: inherit
}

details {
  display: block
}

summary {
  display: list-item
}

template {
  display: none
}

[hidden] {
  display: none
}

*,*:before,*:after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  vertical-align: baseline
}

a img {
  border: none
}

b,strong {
  font-weight: 700
}

button,input[type=button] {
  border: 0
}

em,cite,i {
  font-style: italic
}

img,figure,picture {
  border: 0;
  display: block;
  height: auto;
  max-width: 100%
}

h1,h2,h3,h4,h5,h6 {
  font-weight: 500
}

sub {
  text-transform: lowercase;
  font-size: inherit;
  font-variant-position: sub
}

sup {
  text-transform: lowercase;
  font-variant-position: super
}

textarea {
  overflow: auto;
  resize: vertical
}

@font-face {
  font-family: Metropolis;
  font-weight: 100;
  font-style: normal;
  font-stretch: normal;
  font-display: swap
}

@font-face {
  font-family: Metropolis;
  font-weight: 400;
  font-style: normal;
  font-stretch: normal;
  font-display: swap
}

@font-face {
  font-family: Metropolis;
  font-weight: 900;
  font-style: normal;
  font-stretch: normal;
  font-display: swap
}

body {
  background-color: var(--background-body);
  color: var(--color-body);
  line-height: 1.4;
  font-family: var(--font-body);
  font-feature-settings: "kern" 1,"onum" 0,"liga" 0,"tnum" 1;
  text-rendering: optimizeLegibility;
  word-wrap: break-word
}

h1,h2,h3,h4,h5,h6,p {
  margin: 1rem 0
}

mark {
  background-color: var(--color-highlight);
  padding: 0 .25em
}

a {
  color: var(--color-link)
}

img,video {
  display: block;
  max-width: 100%;
  height: auto
}

button,select,textarea,input[type=submit],input[type=button] {
  appearance: none;
  background-color: var(--background-form);
  border: none;
  border-radius: var(--border-radius);
  color: var(--color-form);
  font-family: var(--font-form);
  font-size: inherit;
  outline: none;
  padding: .5em
}

button,input[type=button],input[type=checkbox],input[type=radio],input[type=range],input[type=submit],select {
  cursor: pointer
}

input[type=button],input[type=range],input[type=submit],select {
  display: inline-block
}

button:hover,input[type=button]:hover,input[type=submit]:hover {
  background: var(--background-form)
}

button:focus,input:focus,select:focus,textarea:focus {
  box-shadow: 0 0 0 2px var(--color-focus)
}

button:disabled,input:disabled,select:disabled,textarea:disabled {
  cursor: not-allowed;
  opacity: .5
}

table {
  border-collapse: collapse;
  width: 100%;
  table-layout: fixed
}

table caption,td,th {
  text-align: left
}

td,th {
  padding: .25em;
  vertical-align: top;
  word-wrap: break-word
}

thead {
  border-bottom: 1px solid var(--color-border)
}

tfoot {
  border-top: 1px solid var(--color-border)
}

::-moz-placeholder {
  color: var(--color-placeholder)
}

:-ms-input-placeholder {
  color: var(--color-placeholder)
}

::-ms-input-placeholder {
  color: var(--color-placeholder)
}

::placeholder {
  color: var(--color-placeholder)
}

::-moz-selection {
  background-color: var(--color-selection)
}

::selection {
  background-color: var(--color-selection)
}

.skip-to-main {
  border: none;
  width: 1px;
  height: 1px;
  overflow: hidden;
  position: absolute;
  background-image: none
}

.skip-to-main:focus {
  background-color: var(--color-off-black);
  color: var(--color-white);
  width: auto;
  height: auto;
  padding: .5em;
  z-index: var(--z-overlay)
}

.sr-only {
  clip: rect(0 0 0 0);
  clip-path: inset(100%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px
}

mark:before,mark:after,del:before,del:after,ins:before,ins:after,s:before,s:after {
  clip: rect(0 0 0 0);
  clip-path: inset(100%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px
}

:root {
  --sans: "Metropolis", Helvetica, Arial, sans-serif;
  --serif: Georgia, Times, serif;
  --mono: Menlo, Consolas, Monaco, "Courier New", monospace;
  --z-bottom: -100;
  --z-middle: 0;
  --z-top: 100;
  --z-overlay: 1000;
  --border-radius: 0px;
  --font-body: var(--sans);
  --font-form: var(--sans);
  --color-accent: var(--color-purple);
  --background-body: var(--color-white);
  --background-form: var(--color-off-white);
  --color-body: var(--color-off-black);
  --color-placeholder: var(--color-gray-dark);
  --color-link: var(--color-off-black);
  --color-link-border: var(--color-off-black);
  --color-focus: var(--color-accent);
  --color-form: var(--color-black);
  --color-border: var(--color-gray-light);
  --color-selection: var(--color-gray-light);
  --color-highlight: var(--color-accent);
  --font-size-giant: clamp(2.5rem, 5.25vw, 6.5rem);
  --font-size-large: clamp(1.5rem, 3.25vw, 3.25rem);
  --font-size-medium: clamp(1.25rem, 2.25vw, 2.25rem);
  --font-size-small: clamp(1rem, 1.25vw, 1.25rem);
  --font-size-xsmall: clamp(.85rem, 1vw, 1rem);
  --font-weight-bold: 900;
  --font-weight-normal: 400;
  --font-weight-thin: 100;
  --width-column-wide: 1500px;
  --width-column-regular: 720px;
  --width-padded: 80vw;
  --margin-left: 10vw;
  --width-padded-mobile: 90vw;
  --margin-left-mobile: 5vw;
  --transition-fast: .1s;
  --transition-medium: .2s;
  --transition-slow: .5s;
  --transition-ease: ease-in
}

body {
  font-size: 16px
}

/*h1,h2 {*/
/*  font-size: var(--font-size-large);*/
/*  font-weight: var(--font-weight-bold);*/
/*  color: var(--color-off-black);*/
/*  line-height: 1;*/
/*  margin-top: 2em*/
/*}*/

h3 {
  font-size: var(--font-size-medium);
  font-weight: var(--font-weight-bold);
  color: var(--color-off-black);
  margin-top: 2em
}

h4 {
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-bold);
  color: var(--color-off-black)
}

p {
  font-size: var(--font-size-small);
  line-height: 1.65
}

li {
  font-size: var(--font-size-small);
  line-height: 1.65;
  margin-bottom: 1em
}


a:hover,a:focus {
  background-size: 100% 100%;
  outline: none
}

button:hover,button:focus,a.btn:hover,a.btn:focus {
  background-image: linear-gradient(90deg,var(--color-accent) 50%,var(--color-accent) 50%)
}

.wordmark a {
  text-decoration: none;
  background-image: none
}
a.solid svg,.round-svg svg {
  fill: var(--color-off-black);
  stroke: none
}

.solid svg:hover,.round-svg svg:hover {
  fill: var(--color-accent)
}

a.stroke svg:hover {
  stroke: var(--color-accent)
}
.logo a,.logo a:hover {
  text-decoration: none;
  background-image: none
}
.logo svg {
  display: block
}

.banner a {
  color: var(--color-white);
  border-bottom: 2px solid currentColor
}
.btn-open>* {
  pointer-events: none
}
a {
  text-decoration: none;
  color: var(--color-link);
  background-image: linear-gradient(var(--td-brand-color-5),var(--td-brand-color-3));
  background-size: 100% .1em;
  background-position: 0 90%;
  background-repeat: no-repeat;
  transition: all var(--transition-fast) var(--transition-ease);
  padding: 0 .5em;
}

a:hover,a:focus {
  background-size: 100% 100%;
  outline: none
}
span {
  font-size: 20px;
  font-family: "KaiTi";
}

</style>
