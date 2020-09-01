
let register_app = new Vue({
	el:'#register_app',
	data:{
        register_name:'',
        user_name_msg:'',
        email:'',
        pwd:'',
        pwd2:'',
        is_register:0,
        msg:'',
        email_msg:'',
        pwd_msg:'',
        pwd2_msg:'',

     
	},
	methods:{
		toLogin(){
			// console.log(this.path)
			window.location = loginPath
			// window.open('index.html')
        },
        verify_user_name(){
            if(this.register_name.length<=5){
                return
            }
            
            let app = this
            // 验证用户名是否存在
            axios.get(actPath+"userinfo.action/?user_name="+app.register_name).then(function(response){
                if(response.data.id){
                    app.msg = '用户名已存在！'
                }else{
                    app.msg = ''
                }
                
            })
        },
        verify_email(){
            // alert('wwwwww')
            // 验证邮箱是否存在
            let r1 = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/
            if(!r1.test(this.email)){
                return
            }

            let app = this
            // 验证邮箱是否已被注册
            axios.get(actPath+"userinfo.action/?email="+app.email).then(function(response){
                if(response.data.id>1){
                    app.msg = '邮箱已被注册！'
                }else{
                    app.msg = ''
                }
                
            })

        },
        verify_user_name_reg(){
            // console.log(this.register_name)
            let r1 = /^(?![0-9])[_a-zA-Z0-9]+$/
            if(this.register_name.replace(/[^\x00-\xff]/g,'AA').length<=5){
                this.user_name_msg='*用户名长度不应小于5'
            }
            else if(this.register_name.replace(/[^\x00-\xff]/g,'AA').length>=25){              
                this.user_name_msg='*用户名长度不应大于25'
            }else if(!r1.test(this.register_name)){
                this.user_name_msg='*用户名只能由数字、字母、下划线组成，且不能由数字开头'
            }else{
                this.user_name_msg=''
            }
        },
        verify_email_reg(){
            let r1 = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/
            if(!r1.test(this.email)){
                this.email_msg='*请输入正确的邮箱'
            }else{
                this.email_msg=''
            }
        },
        
        verify_pwd_reg(){
            let r1 = /^[_a-zA-Z0-9]+$/
            // console.log(r1.test(this.pwd))
            if(!r1.test(this.pwd)){              
                this.pwd_msg='*密码只能由数字、字母、下划线组成'
            }else if(this.pwd.length<=6){
                
                this.pwd_msg='*密码长度应该不小于6位'
            }else{
                this.pwd_msg=''
            }
        },
        verify_pwd2_reg(){
            
            if(this.pwd != this.pwd2){
                
                this.pwd2_msg = '两次密码不一致'
            }else{
                this.pwd2_msg = ''
            }
        },
        async register(){

            if(this.msg){
                alert(this.msg)
                return
            }
            if(
                !this.register_name || !this.email || !this.pwd || !this.pwd2
            ){
                alert('请填满所有表单项！！')
                return
            }else if(
                this.pwd_msg || this.pwd2_msg || this.user_name_msg || this.email_msg
            ){
                alert('请输入正确的值！')
                return
            }
            let app = this
            
            let data = {
                user_name: app.register_name,
                email: app.email,
                user_password : app.pwd,
            }
            // 未完成：为空时抛出请输入账号、密码
            // await this.$api.common
            // .addImg(data, {
            // headers: { "Content-Type": "multipart/form-data" }
            // })
            
            await axios({
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                method: 'post',
                url: actPath+"register.action/",
                data: 
                    Qs.stringify(data)
                
            }).then(function(response){
                app.is_register = response.data.is_register
                app.msg = response.data.msg
            });
            
            // 测试：
            // alert('注册状态'+ app.is_register+'\n')

            // 如果is_register=1,跳转到我的空间
            if (app.is_register==1){
                alert('请到邮箱验证您的注册！即将跳转到主页！')
                window.location=indexPath
            }else{
                alert('由于服务器问题，注册失败！')
            }

        }
		
    }
    
})