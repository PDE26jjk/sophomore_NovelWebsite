
// 获取搜索关键词
let path = window.document.location.href.toString();
var search_key_get = decodeURI(path.split("#")[1])

let main = new Vue({
	el:'#main',
	data:{
        type: 0,
        search_key: search_key_get,
        search_result_art:[],
        search_result_user:[],
        search_station:"作品",
        
	},
	methods:{
        change_station(station){
            this.search_station = station
            this.search()

        },
		async search(){
            let app = this
            let key = this.search_key
            key = key.trim()
            
			if(key !== ''){
                window.location = searchPath +'#' +key
                
            }

            if(this.search_station =="作品"){
                axios.get(actPath+"artsearch.action/?q=7&order=1&key="+key).then(function(response){
                    main.search_result_art = response.data.works
                    _updatefooter()	
                })
            }
            if(this.search_station =="用户"){
                axios.get(actPath+"usersearch.action/?q=7&order=1&key="+key).then(function(response){
                    main.search_result_user = response.data.users                    
                    _updatefooter()	
                })
            }
            		
        },
        
        
	},created:async function(){
        let app = this
        if(app.search_key){
            await axios.get(actPath+"artsearch.action/?q=7&order=1&key="+app.search_key).then(function(response){

                main.search_result_art = response.data.works
            })

        }
       
    },
})
