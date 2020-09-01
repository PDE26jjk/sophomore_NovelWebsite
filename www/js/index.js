// 注册码注册
let path = window.document.location.href.toString();
if(path.indexOf("#") != -1){
	let vc = decodeURI(path.split("#")[1])
	axios.get(actPath+"verification.action/?vc="+vc)
	.catch(function (error) {
		// handle error
		console.log(error);
	  }).then(function(response){
		let is_success = response.data.is_success
		let msg = response.data.msg
		if(is_success == 1){
			alert(msg)
			window.location = indexPath
			location.reload()
		}else{
			window.location = indexPath
		}

	})
}


memu = new Vue({
	el:'#memu',
	data:{
		type: 0,
		list:['武侠','玄幻','都市','军事','游戏','科幻','现实','历史','言情','体育','悬疑','更多']

	},
	methods:{
		toType:function(type){
			// this.type = list.indexOf(type)
			window.location = typePath+'#'+type
		}
	},
	
})

index_app = new Vue({
	el:'#index_app',
	data:{
		rank_list:[],
		hot_list:[],
		recommend_list:[],
		mediaPath:mediaPath,
		

	},
	computed:{
		big_pic:function(){
			if(this.hot_list[0])
				return mediaPath+this.hot_list[0].pic
		},
		big_title:function(){
			if(this.hot_list[0])
				return this.hot_list[0].title
		},
		now_time:function(){
			return new Date().getTime()
		}
		
	},
	methods:{
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
	},
	
	beforeMount:async function(){
		let app = this
        await axios.get(actPath+"getworks.action/?order=1&pattern=1&q=10&type=").then(function(response){
			if(response.data.works)
				app.rank_list=response.data.works
		})
		await axios.get(actPath+"getworks.action/?order=1&pattern=2&q=5&type=").then(function(response){

			if(response.data.works){
				app.hot_list=response.data.works		
			}

		})
		await axios.get(actPath+"getworks.action/?order=1&pattern=3&q=4&type=").then(function(response){
			if(response.data.works)
				app.recommend_list=response.data.works
		})
	},
})