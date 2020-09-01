

// 获取分类
let path = window.document.location.href.toString();
var type_get = decodeURI(path.split("#")[1])
// alert(decodeURI(type))
    


memu = new Vue({
	el:'#memu',
	data:{
        // 将分类绑定到vue
        type : type_get,
		list:['武侠','玄幻','都市','军事','游戏','科幻','现实','历史','言情','体育','悬疑','更多']
	},
	methods:{
		toType:function(type){
            // alert(typePath+'#'+type)
            window.location = typePath+'#'+type
            location.reload()
		}
    }
    
})

type_app = new Vue({
	el:'#type_app',
	data:{
		rank_list:[],
		hot_list:[],
		recommend_list:[],
		mediaPath:mediaPath,
	},
	computed:{
		big_pic:function(){
			if(this.hot_list)
			if(this.hot_list[0])
				return mediaPath+this.hot_list[0].pic
		},
		big_title:function(){
			if(this.hot_list)
			if(this.hot_list[0])
				return this.hot_list[0].title
		},
		now_time:function(){
			return new Date().getTime()
		}
		
	},
	methods:{
		getpic:function(item){
			if (item)
			return item.pic
		},
		toType:function(type){
			// this.type = list.indexOf(type)
			window.location = typePath+'#'+type
		},time:function(date){
			let pub_time = new Date(date).getTime()
			let now = this.now_time
			return _getTime(now-pub_time)
		},tobigbook(){
			window.location=detailPath+'#'+ this.hot_list[0].id
		}
    },created:async function(){
		let app = this
        await axios.get(actPath+"getworks.action/?order=1&pattern=1&q=10&type="+type_get).then(function(response){
			if(response.data.works)
				app.rank_list=response.data.works
		})
		await axios.get(actPath+"getworks.action/?order=1&pattern=2&q=5&type="+type_get).then(function(response){
			if(response.data.works){
				console.log(response.data.works)			
					app.hot_list=response.data.works
			}

		})
		await axios.get(actPath+"getworks.action/?order=1&pattern=3&q=4&type="+type_get).then(function(response){
			if(response.data.works)
				app.recommend_list=response.data.works
		})
	},
    
})
