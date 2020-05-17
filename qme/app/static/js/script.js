// Handle socket to send /receive messages from server without refresh
$(document).ready(function(){

});

// tables.js
function preg_quote( str ) {
  // http://kevin.vanzonneveld.net
  // +   original by: booeyOH
  // +   improved by: Ates Goral (http://magnetiq.com)
  // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  // +   bugfixed by: Onno Marsman
  // *     example 1: preg_quote("$40");
  // *     returns 1: '\$40'
  // *     example 2: preg_quote("*RRRING* Hello?");
  // *     returns 2: '\*RRRING\* Hello\?'
  // *     example 3: preg_quote("\\.+*?[^]$(){}=!<>|:");
  // *     returns 3: '\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:'
  return (str+'').replace(/([\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:])/g, "\\$1");
}

function highlight( data, search ){
  return data.replace(new RegExp( "(" + preg_quote( search ) + ")" , 'gi' ), "<mark>$1</mark>" );
}
    
function Table($table,$input){

    $table.find("th").each(function($key, el){
        if ($(el).attr("data-sorting")!="disabled"){
            $("<span/>").attr("class","fa").attr("row-id",$key+1).appendTo(el);
    }}).click(function(){
        var asc=true;
        if ($(this).find("span.fa").attr("class")=="fa"||$(this).find("span.fa").attr("class")=="fa fa-caret-up fa-fw"){
            $table.find("th[data-sorting!=disabled] span.fa").attr("class","fa");
            $(this).find("span.fa").attr("class","fa fa-caret-down fa-fw");
        asc=true;
        }
        else if ($(this).find("span.fa").attr("class")=="fa fa-caret-down fa-fw"){
            $table.find("th[data-sorting!=disabled] span.fa").attr("class","fa");
            $(this).find("span.fa").attr("class","fa fa-caret-up fa-fw");
            asc=false
        }
        value=$.map($table.find("td:nth-child("+($(this).find("span.fa").attr("row-id"))+")"),function(el){
            return {text:$(el).text().trim(),row:$(el).parent()};
        });

        value.sort(function(x, y){ 
            if (asc){
                if (x.text < y.text) {
                    return -1;
                }
                if (x.text > y.text) {
                    return 1;
                }
            } else {
                if (x.text < y.text) {
                    return 1;
                }
                if (x.text > y.text) {
                    return -1;
                }
            }
            return 0;
        });
        $table.find("tr:gt(0)").remove();
        $.each(value,function(key,value){
            $(value.row).appendTo($table);
        });
    });
    $table.find("th:first").click();
    $input.on("keyup change",function(){
        var newText=$(this).val();
        $table.find("span.text-wrap").each(function(key,value){
            $(value).html($(value).text());
            $(value).contents().unwrap();
        });        
        if (newText.trim()!=""){    
            $table.find("tr:gt(0)").hide();                        
            var textNode=$table.find("tr:gt(0) *")
              .contents()
              .filter(function() {
                return this.nodeType === 3; //Node.TEXT_NODE
              }).each(function(key,value){
                    var nodeText=value.data;
                    if (nodeText.toLowerCase().indexOf(newText.toLowerCase())!=-1){
                        $(value).closest("tr").show();
                        if ($(value).parent().attr("class")!="text-wrap")
                            $(value).wrap("<span class='text-wrap'></span>");
                        $(value).parent().html(highlight(nodeText ,newText));
                    }
                
              });;
              
              }else{
                $table.find("tr").show();
              }
    });
    
}

// Table

$(function(){
    Table($(".table-sortable"),$(".table-sortable-search"));
});

// Search

$('input[type="search"]').keyup(function () {
  var t = $(this);
  t.next('span').toggle(Boolean(t.val()));
});

$('input[type="search"] + .search-cancel-button').hide($(this).prev('input').val()).click(function () {
  $(this).prev('input').val('').focus();
  $(this).hide();
});

const app = new Vue({
  data: () => ({
    rows: [],
    newRow: { name: '', command: '' },
    sort: 'id',
    sortDir:'asc',
    page: 0,
    pageSize: 25
  }),
  created: function() {

      // Reference for app later
      var self = this

      // connect to the socket server update endpoint      
      this.socket =  io.connect('http://' + document.domain + ':' + location.port + '/update');
      this.socket.on('connect', function() {
        console.log('Websocket connected!');
      });

      // receive new rows from the server, update table
      this.socket.on('FSdatabase', function(msg) {
        self.rows = []
        $.each(msg.rows, function(i, row){
          self.rows.push({
            id:      i,
            executor: row[0],
            name:    row[1],
            command: row[2],
          });
        })
      });

  },
  methods: {
    addRow: function() {
      let name    = this.newRow.name.trim().toLowerCase();
      let surname = this.newRow.command.trim().toLowerCase();
      if (name && surname) {  
        this.rows.push({
          id:      this.rows.length,
          name:    name,
          surname: surname
        });
        this.sortDir = 'desc'; this.sortBy('id'); // Default sorting
      }
      this.newRow.name = this.newRow.command = '';
    },
    sortBy: function(s) {
      if (s === this.sort) {
        this.sortDir = (this.sortDir === 'asc') ? 'desc' : 'asc';
      } else {
        this.sortDir = 'asc';
      }
      this.sort = s;
    },
    isActiveSort: function(s) { 
      return this.sort === s; 
    },
    hasPage: function(dir) {
      if (dir === -1 && (this.page > 0)) return true;
      if (dir ===  1 && (((this.page+1)*this.pageSize) < this.rows.length)) return true;
      return false;
    },
    prevPage: function() {
      if (this.hasPage(-1)) this.page--;
    },
    nextPage: function() {
      if (this.hasPage(1)) this.page++;
    }
  },
  computed: {
    sortedRows: function() {
      return this.rows.sort((a, b) => {
        let dir = (this.sortDir === 'asc') ? 1 : -1;
        if (a[this.sort] < b[this.sort]) {
          return -1 * dir;
        } else if (a[this.sort] > b[this.sort]) {
          return  1 * dir;
        } else {
          return 0;
        }
      }).filter((row, idx) => {
        let s = this.page*this.pageSize;
        let e = (this.page+1)*this.pageSize;
        return (idx >= s && idx < e);
        });
    },
    pageSizeModel: {
      get() {
        return this.pageSize;
      },
      set(v) {
        this.pageSize = v;
        this.page = 0;
      }
    }
  },
  filters: {
    capitalize: function (v) {
      if (!v) return ''
      v = v.toString()
      return v.charAt(0).toUpperCase() + v.slice(1)
    }
  }
}).$mount('#app');
