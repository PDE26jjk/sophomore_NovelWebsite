// 页面文件，上线后记得改成。。。
const registerPath = 'register.html'
const loginPath = 'login.html'
const indexPath = 'index.html'
const typePath = 'type.html'
const spacePath = 'space.html'
const searchPath = 'search.html'
const articlePath = 'article.html'
const detailPath = 'detail.html'
const commentPath = 'comment.html'
const userinfoPath= 'userinfo.html'
// 动态内容的域名
const actPath = 'http://127.0.0.1:8000/'
const mediaPath = actPath + 'media/'
const _mediaPath = mediaPath
// Vue.prototype.$axios = axios;

// 发请求带上sessionID
axios.defaults.withCredentials=true;

// document.body.scrollHeight
let base = new Vue({
	el:'#base',
	data:{
		is_login : 0,
		path : window.location.href,
		search_key: '',
		user_id:0,
		avatar:'',

	},
	methods:{
		index(){
			window.location = indexPath
		},
		register(){
			// console.log(this.path)
			window.location = registerPath
			// window.open('index.html')
		},
		login(){
			window.location = loginPath
		},
		space(){
			window.location = spacePath
		},
		tomy_coll(){
			window.location = spacePath + '#' +2
			
		},
		tomy_comment(){
			window.location = spacePath + '#' +1
			
		},
		tomy_sub(){
			window.location = spacePath + '#' +3
			
		},
		search_input_focus(){
			$('.search_div').css('border-color', 'rgb(228,106,94)')
		},
		search_input_blur(){
			$('.search_div').css('border-color', 'rgb(94,88,79)')
		},
		search(){
			let key = this.search_key
			key = key.trim()
			if(key !== ''){
				window.location = searchPath +'#' +this.search_key
				
			}
			
		}

	},
	beforeMount:async function(){
        await axios.get(actPath+"userstation.action/").then(function(response){
			base.is_login = response.data.is_login
			base.user_id = response.data.user_id
			base.avatar = response.data.avatar
			
		})
	},
	created:async function(){
		
		setTimeout(function (){
			let pH = document.body.scrollHeight
					$('.footer').css('top',(pH+100)+'px')
			
		}, 1000);
		setTimeout(function (){
			let pH = document.body.scrollHeight
			$('.footer').css('top',(pH+100)+'px')
				
			}, 1000);
		
	}
})


var is_login = 0
// 用户状态获取

// 将时间撮转换为时间差，格式化显示
var _getTime =function(stamp){
	var days=Math.floor(stamp/(24*3600*1000))  
	var years = days%(365.25)
	var months = days%(365.25/12)
    //计算出小时数    
    var hours=Math.floor(stamp/(3600*1000))  
    //计算相差分钟数  
    var minutes=Math.floor(stamp/(60*1000))  
    //计算相差秒数  
	var seconds=Math.round(stamp/1000) 
	if(seconds<10){
		return '刚刚'
	} 
    if(minutes<1){
		return seconds + '秒前'
	} 
	if(hours<1){
		return minutes + '分钟前'
	} 
	if(days<1){
		return hours + '小时前'
	}
	if(days<31){
		return days + '天前'
	}
	if(days<365.25){
		return months + '月前'
	}
	if(days>365.25){
		return years + '年前'
	}
	return '时间错误'
};
// 将过去时间格式化显示
var _time = function(time){
	let pub_time = new Date(time).getTime()
	let now = new Date().getTime()
	return _getTime(now-pub_time)
}

var _tobook=function(id){
	window.location = detailPath + '#' + id
}
var _tochapter=function(id){
	window.location = articlePath + '#' + id
}
var _tocomment=function(id){
	window.location = commentPath + '#' + id
}
var _totype=function(type){
	window.location = typePath + '#' + type
}

var _touserinfo=function(user_id){
	window.location = userinfoPath + '#' + user_id
}
// 实现简单分页
var _getPage=function(list,num){
	l = []
	allpage= Math.ceil(list.length/num)
	for(i=0;i<allpage;i++){
		l.push(list.splice(0,num))
	}
	return l
}
var _index=function(){
	window.location = indexPath
}
var _updatefooter= function(){
	setTimeout(function (){
		let pH = document.body.scrollHeight
		$('.footer').css('top',(pH+100)+'px')
			
	}, 500);
}



