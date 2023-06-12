<template>
<div>
  <transition-group name="changeShow" appear>
    <h1 v-show="showDiv-1>=0" key="1"> Movie Box</h1>
    <t-divider key="3"></t-divider>
    <h1 v-show="showDiv-2>=0" key="2"> World Cloud</h1>
    <t-divider></t-divider>
    <h1 v-show="showDiv-3>=0" key="3">Analyzing</h1>
  </transition-group>
</div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      showDiv: 0
    }
  },
  methods: {
    aboutDiv : function () {
      setInterval(()=>{
        this.showDiv +=1
      },200)

    }
  },
  mounted() {
    this.aboutDiv()
  }
}
</script>

<style scoped>
h1 {
  background-color: wheat;
  padding: 2em;
  height: 5em;
  margin: 30px;
}

.changeShow-enter,
.changeShow-leave-to {
  transform: translateX(-100%);
}

.changeShow-enter-active,
.changeShow-leave-active {
  transition: 0.8s linear;
}

.changeShow-enter-to,
.changeShow-leave {
  transform: translateX(0);
}
</style>
