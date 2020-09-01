
let login_app = new Vue({
	el:'#login_app',
	data:{
        login_name:'',
        pwd:'',
        is_login: 0,
        msg:'',

	},
	methods:{
		toRegister(){
			// console.log(this.path)
			window.location = registerPath
			// window.open('index.html')
        },
        
        async login(){
            let app = this
            
            let data = {
                user_name: app.login_name,
                user_password : app.pwd
            }
            // 未完成：为空时抛出请输入账号、密码
            // await this.$api.common
            // .addImg(data, {
            // headers: { "Content-Type": "multipart/form-data" }
            // })
            let user_name = "你没登录！"
            await axios({
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                method: 'post',
                
                url: actPath+"login.action/",
                data: 
                    Qs.stringify(data)
                
            }).then(function(response){
                app.is_login = response.data.is_login
                app.msg = response.data.msg
                user_name = response.data.user_name
            });
            
            
            // 测试：
            // alert('登录状态：'+ app.is_login+'\n如果is_login=1,跳转到我的空间')

            // 如果is_login=1,跳转到我的空间
            if (app.is_login==1){
                alert("欢迎回来，"+user_name+"!")
                window.location=indexPath
            }else if(app.is_login==0){
                alert("用户名或密码错误！")
            }

        }
		
    }
    
})
