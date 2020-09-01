// 获取小说ID
let path = window.document.location.href.toString();
var art_id_get = decodeURI(path.split("#")[1])
// alert(art_id_get)


let detail_app = new Vue({
	el:'#detail_app',
	data:{
        title:'',
        type:'',
        author_id:'',
        author:"",
        pub_time:"",
        content:"",
        chapter:[],
        chapter_id:[],
        com_num:1000,
        is_like:0,
        is_coll:0,
        font_size:14,

	},
	methods:{
        
		toIndex(){
            window.location= indexPath
        },
        tochapter(index){
            // alert(index)
            window.location=articlePath+'#'+this.chapter_id[index]
        },
        tocomments(){
            window.location= commentPath + "#" + art_id_get
        },
        toType(){
            window.location=typePath+'#'+this.type
        },
        async like(){
            let app = this
            await axios.get(actPath+"addlike.action/?id="+art_id_get).then(function(response){
                if(response.data.is_success==1){
                    app.is_like=!app.is_like
                }else if(response.data.is_success==-1){
                    alert(response.data.msg)
                    window.location=loginPath
                }else{
                    alert('操作失败！')
                }
            }).catch(err=>{
                alert('由于服务器问题，操作失败！')
            })
        },
        async coll(){
            let app = this
            await axios.get(actPath+"addcoll.action/?id="+art_id_get).then(function(response){
                if(response.data.is_success==1){
                    app.is_coll=!app.is_coll
                }else if(response.data.is_success==-1){
                    alert(response.data.msg)
                    window.location=loginPath
                }else{
                    alert('操作失败！')
                }
            }).catch(err=>{
                alert('由于服务器问题，操作失败！')
            })
        },
        fzup(){
            if(this.font_size<=26){
                 $('.art_abstract_content p').animate({ fontSize: '+=2px' })
                 this.font_size +=2
            }          
        },
        fzdown(){
            if(this.font_size>=8){
                $('.art_abstract_content p').animate({ fontSize: '-=2px' })
                this.font_size -=2
           }
        }
    },
    computed:{
        content_str:function(){
            
            return this.content.split('\n')
        }
    },
    created:async function(){
        let app = this
        await axios.get(actPath+"article.action/?id="+art_id_get).then(function(response){
            if(response.data.book_id){            
                if(response.data.book_id!= art_id_get){
                    // 如果不是整本，则跳转到整本页面
                    window.location = detailPath + "#" + response.data.book_id
                    location.reload()
                }else{
                    console.log(response.data)
                    app.title = response.data.title
                    app.type = response.data.type
                    app.content = response.data.content
                    app.author = response.data.author
                    app.author_id= response.data.author_id
                    app.chapter = response.data.chapters
                    app.chapter_id = response.data.chapters_id
                    app.pub_time = response.data.pub_time
                    app.book_id = response.data.book_id
                    app.com_num = response.data.com_num
                    app.is_like = response.data.is_like
                    app.is_coll = response.data.is_coll
                }
            }
        })
    },
    beforeMount:function(){
        if(this.book_id != art_id_get){
            // window.location = detailPath + "#" + this.book_id
            // location.reload()
            // alert(this.book_id)
        }
    }


})
