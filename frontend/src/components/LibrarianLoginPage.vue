<template>
    <LoginForm :title="'Librarian Login'" :isLibrarian="true" @login = "handleChildSubmit"  class="vh-100 d-flex justify-content-center align-items-center"/>
</template>

<script>
import LoginForm from './LoginForm.vue';

export default {
    name: 'LibrarianLoginPage',
    components: {
        LoginForm
    },
    methods: {
        handleChildSubmit(data){
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            const raw = JSON.stringify({
            "username": data.email,
            "password": data.password
            });

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };

            fetch("http://127.0.0.1:5000/librarian/login", requestOptions)
            .then((response) => {
                if (response.status === 200) {
                    return (response.json())
                } else if (response.status === 401) {
                    window.alert('Invalid Credentials');
                } else if (response.status === 500) {
                    window.alert('Internal server error');
                } else {
                    window.alert('Unexpected status code:', response.status);
                }
            })
            .then((data) => {
                if (data) {
                    localStorage.setItem('user_token', data.token);
                    localStorage.setItem('user', data.username);

                    // window.alert('Successful Login!');
                    setTimeout(() => {
                        window.location.href = '/librarian/dashboard';
                    }, 500);
                }
            })
            .catch((error) => {
            console.error('Fetch error:', error);
            });
        }
    }
}
</script>