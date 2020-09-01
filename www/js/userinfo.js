// 获取用户id
let path = window.document.location.href.toString();
var user_id_get = decodeURI(path.split("#")[1])

let main = new Vue({
	el:'#main',
	data:{
        name:'',
        nickname:"",
        avatar:'',
        com_page:0,
        intro:'',
        like_list:[],
        work_list:[],
        coll_list:[],
        sub_list:[],
        is_sub:0,
	},
	methods:{
        async subscribe(){
            let app = this
            await axios.get(actPath+"addsub.action/?id="+user_id_get).then(function(response){
                if(response.data.is_success==1){
                    app.is_sub=!app.is_sub
                }else if(response.data.is_success==-1){
                    alert(response.data.msg)
                    window.location=loginPath
                }else{

                    alert(response.data.msg+'操作失败！')
                }
            }).catch(err=>{
                alert('由于服务器问题，操作失败！')
            })
        },
        touserinfo(user_id){
            window.location = userinfoPath + '#' + user_id
            location.reload()
        }

        
        
	},created:async function(){
        let app = this
        if(user_id_get){
            axios.get(actPath+"getusershowinfo.action/?id="+user_id_get).then(function(response){
                console.log(response.data);
                app.like_list=response.data.likes
                app.sub_list=response.data.subs
                app.work_list=response.data.works
                app.coll_list=response.data.colls
                app.is_sub=response.data.is_sub
                app.name=response.data.user.name
                app.nickname=response.data.user.nickname
                app.avatar=response.data.user.avatar
                app.intro=response.data.user.intro
            })

        }
       
    },
})
