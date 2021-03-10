var vue = new Vue({
  el:'#app',
  delimiters: ['[[',']]'],
  return: {
    data:{
    zs_names:['上证指数','深证成指','创业板指'],
    zs_values:[],
    jj_values:[],
    show: false,
    sortType:'gszzl'}
  },
  methods: {
    sort(type) {
      this.sortType = type;
      this.jj_values = this.jj_values.sort(this.compare(type));
    },
    compare(attr) {
      return function(a,b){
      var val1 = a[attr];
      var val2 = b[attr];
      return val2 - val1;
      }
    }
  },
  created() {
    var socket = io();
    socket.on('connect', function() {
      socket.emit('my event', data = 'I\'m connected!');
    });
    socket.on('zs', (zs,jj)  => {
      this.zs_values = zs;
      this.jj_values = jj;
      this.sort(this.sortType);
      this.show = true
      console.log(this.jj_values);
    });
  }
});