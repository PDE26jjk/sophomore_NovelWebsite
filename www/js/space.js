// 获取标签
let path = window.document.location.href.toString();
var lable_get = decodeURI(path.split("#")[1])

// alert(art_id_get)


let space_app = new Vue({
	el:'#space_app',
	data:{
        lable_list:[['fa-star','我的点赞'],['fa-comments','我的评论'],['fa-heart','我的收藏'],['fa-bell','我的订阅'],['fa-book','作品上传'],['fa-user','个人信息'],['fa-cog','隐私设置']],
        lable_selected:-1,
        is_cre:0,
        works:[],
        user_id:0,
        is_book:0,
        pub_content:"",
        pub_title:"",
        book_id:0,
        book_type:"",
        like_list:[],
        coll_list:[],
        sub_list:[],
        com_list:[],
        com_list_length:0,
        name:'',
        nickname:"",
        avatar:'',
        com_page:0,
        intro:'',
        
	},
	methods:{
		logout(){
            axios.get(actPath+"logout.action/")
            window.location= indexPath
        },
        tobook(id){
            window.location=detailPath+'#'+id
        },
        tochapter(id){
            window.location=articlePath+'#'+id
        },
        changelable(index){
            this.lable_selected = index
            window.location = spacePath+'#'+this.lable_selected
        },
        addchapter(book_id){
            this.is_cre=1
            this.is_book=0
            this.book_id = book_id
            //workupload.action
            
        },
        addbook(){
            this.is_cre=1
            this.is_book=1
            this.book_id = 0
            
        },
        publish(){
            if(!this.pub_title || !this.pub_content){
                alert('请勿上传空内容！！')
                return
            }                    
            if(!this.is_book){
                
                let data = {
                    'book_id': this.book_id,
                    'title': this.pub_title,
                    'content' :this.pub_content,
                }
                // alert(this.book_id)
                axios({
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    method: 'post',
                    url: actPath+"workupload.action/",
                    data: 
                        Qs.stringify(data)
                    
                }).then(function(response){
                    if(response.data.msg)
                        alert(response.data.msg)
                    else
                        alert('发布失败！')
                    if(response.data.is_success)
                        location.reload()
                });

            }else{
                var that = this;
                var inputDOM = that.$refs.inputer;
                var file = inputDOM.files;
                var formData = new FormData();
                formData.append('file', file[0]);
                formData.append('title',this.pub_title)
                formData.append('content',this.pub_content)
                formData.append('book_type',this.book_type)

                $.ajax({ 
                    url: actPath+"workupload.action/",
                    type: "post", 
                    data: formData, 
                    processData: false, 
                    //带上cookie
                    xhrFields: {
                        withCredentials: true
                    },
                    // contentType: 'multipart/form-data', 
                    contentType: false,
                    success: function(data) {
                        alert(data.msg)
                        if(data.is_success){
                            location.reload()
                        }
                    },
                    error: function(error){
                        alert(error.msg)
                    }
                });
            }

        },show_chapter(index){
            $('#work_'+index).toggle()
        },get_com_text(com){           
            if(com.rep_user_name){
                return '@'+ com.rep_user_name +': '+com.content
            }else{
                
                return com.content
            }
        }, 
        changepic(){
            // 修改头像，借鉴 https://www.jb51.net/article/145157.htm
            $('#my_av_space').css('display','none')
            var reads = new FileReader();
            f = document.getElementById('av_file').files[0];
            reads.readAsDataURL(f);
            reads.onload = function(e) {
            document.getElementById('pic_up').src = this.result;
                $("#pic_up").css("display", "block");
            };
        },
        upload_info(){
            var that = this;
                var inputDOM = that.$refs.av;
                var file = inputDOM.files;
                var formData = new FormData();
                formData.append('file', file[0]);
                formData.append('nickname',this.nickname.trim())
                formData.append('intro',this.intro.trim())

                $.ajax({ 
                    url: actPath+"changeinfo.action/",
                    type: "post", 
                    data: formData, 
                    processData: false, 
                    //带上cookie
                    xhrFields: {
                        withCredentials: true
                    },
                    // contentType: 'multipart/form-data', 
                    contentType: false,
                    success: function(data) {
                        alert(data.msg)
                        if(data.is_success==-1){
                            window.location=loginPath
                        }else
                        if(data.is_success==1){
                            location.reload()
                        }
                    },
                    error: function(error){
                        alert(error.msg)
                    }
                });
        }
    },
    computed:{
       com_listbypage(){
           let l = this.com_list
            
            return _getPage(l,4)
        }
    },
    created: function(){
        
    },
    beforeMount:async function(){
        
        if(lable_get != -1)
            this.lable_selected = lable_get
        app = this
        await axios.get(actPath+"userstation.action/").then(function(response){
                app.user_id = response.data.user_id                
        })
        if (app.user_id){            
            await axios.get(actPath+"workbyuser.action/?id="+base.user_id).then(function(response){
                app.works = response.data.works
                // console.log(app.works)
                
            })
        }
        await axios.get(actPath+"myinfo.action/").then(function(response){
            app.like_list=response.data.likes
            app.sub_list=response.data.subs
            app.coll_list=response.data.colls
            app.com_list=response.data.coms
            app.com_list_length=response.data.coms.length
            app.name=response.data.user.name
            app.nickname=response.data.user.nickname
            app.avatar=response.data.user.avatar
            app.intro=response.data.user.intro

        })
    }


})
