
// 获取小说ID
let path = window.document.location.href.toString();
var art_id_get = decodeURI(path.split("#")[1])
// alert(art_id_get)

let comment_app = new Vue({
	el:'#comment_app',
	data:{
        avatar:base.avatar,
        title:'',
        type:'',
        author:"",
        pub_time:"",
        content:"",
        chapter:[],
        chapter_id:[],
        index:1,
        mediaPath:mediaPath,
        comment_text : '',
        art_id:0,
        comments:[],
        is_login:base.is_login,
        is_rep:0,
        rep_user_name:'',
        rep_content:'',
        rep_user:0,
        anc_comment:0,
        recommend_list:[],
        com_num:0,

    },watch:{

    },
    computed:{
        getavatar(){
            return _mediaPath+base.avatar
        }
    },
	methods:{
        get_pic(work){
            if(work)
                return mediaPath + work.pic
            
        },
		toIndex(){
            window.location= indexPath
        },todetail(){
            window.location= detailPath + "#" + this.art_id
        },time(time){
            let pub_time = new Date(time).getTime()
            let now = new Date().getTime()
            return _getTime(now-pub_time)
        },
        add_rep_user_text(text,con,rep){
            if(con.user.id===rep.rep_user){
                return text
            }else{
                console.log()
                console.log(rep)
                return '@'+ rep.rep_user_name +': '+text
            }
        },
        get_user_nameornick(con){
            if(con.user.nickname)
                return con.user.nickname
            return con.user.name
        },
        async comment(){
            let comment_text = this.comment_text.trim()
            if (comment_text.length <10){
                alert('评论内容不能小于10字！')
                return
            }

            let data = {
                art_id:this.art_id,
                anc_comment:0,
                rep_user:0,
                content: this.comment_text,
                
            }
            await axios({
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                method: 'post',
                
                url: actPath+"comment.action/",
                data: 
                    Qs.stringify(data)
                
            }).then(function(response){
                if(response.data.is_success == -1){
                    alert('请登录后再评论！')
                    window.location = loginPath
                }else if(response.data.is_success){
                    alert('评论成功！')
                    location.reload()
                }
            },error => {
                alert('由于服务器问题，评论失败！')
            });

            
        },reply_mask(con,anc_comment){
            if(con.user.nickname){
                this.rep_user_name='回复：@'+con.user.nickname
            }else{
                this.rep_user_name='回复：@'+con.user.name
            }               
            this.rep_user=con.user.id
            this.is_rep=1
            this.rep_content=''
            this.anc_comment=anc_comment
            // alert(this.anc_comment)
            
        },async reply(){
            let rep_content = this.rep_content.trim()
            if (rep_content.length <10){
                alert('回复内容不能小于10字！')
                return
            }

            let data = {
                art_id:this.art_id,
                anc_comment:this.anc_comment,
                rep_user:this.rep_user,
                content: this.rep_content,
            }
            await axios({
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                method: 'post',
                
                url: actPath+"comment.action/",
                data: 
                    Qs.stringify(data)
                
            }).then(function(response){
                if(response.data.is_success == -1){
                    alert('请登录后再评论！')
                    window.location = loginPath
                }else if(response.data.is_success){
                    alert('评论成功！')
                    location.reload()
                }
            },error => {
                alert('由于服务器问题，评论失败！')
            });
        }
    },
    created:function(){
        let app = this
        axios.get(actPath+"article.action/?id="+art_id_get).then(function(response){
            if(response.data.title){
                // console.log(response.data)
                app.title = response.data.title
                app.index = response.data.index
                app.type = response.data.type
                app.content = response.data.content
                app.author = response.data.author
                app.chapter = response.data.chapters
                app.chapter_id = response.data.chapters_id
                app.pub_time = response.data.pub_time
                app.art_id = response.data.id
                app.com_num = response.data.com_num
            }
        })
        // 获取评论
        axios.get(actPath+"getcomments.action/?art_id="+art_id_get).then(function(response){
            console.log(response.data)
            if(response.data.comment){
                app.comments = response.data.comment
                // console.log(app.comments)
            }
        })
        // 获取推荐
        axios.get(actPath+"getworks.action/?order=1&pattern=3&q=5").then(function(response){

			if(response.data.works){
				app.recommend_list=response.data.works		
			}

		})
    }
})
