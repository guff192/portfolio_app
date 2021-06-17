let projects = new Vue({
    el: '#all_projects',
    data: {
        projects: []
    },
    created: function () {
        const vm = this;
        axios.get('/app/api/project')
            .then(function (response) {
                vm.projects = response.data;
            })
    }
});

let companies = new Vue({
    el: '#all_companies',
    data: {
        companies: []
    },
    created: function () {
        const vm = this;
        axios.get('/app/api/company')
            .then(function (response) {
                vm.companies = response.data;
            })
    }
});

let my_companies = new Vue({
    el: '#my_companies',
    data: {
        companies: []
    },
    created: function () {
        const vm = this;
        axios.get('/app/api/my_companies')
            .then(function (response) {
                vm.companies = response.data;
            })
    }
});

let company_projects = new Vue({
    el: '#company_projects',
    data: {
        projects: []
    },
    created: function () {
        const vm = this;
        const url_parts = document.URL.split('/');
        const company_id = url_parts[url_parts.indexOf("companies") + 1];
        axios.get('/app/api/company/' + company_id)
            .then(function (response) {
                console.log(response.data);
                vm.projects = response.data.projects;
            })
    }
});

let company_employees = new Vue({
    el: '#company_employees',
    data: {
        employees: []
    },
    created: function () {
        const vm = this;
        const url_parts = document.URL.split('/');
        const company_id = url_parts[url_parts.indexOf("companies") + 1];
        axios.get('/app/api/companies/' + company_id + '/employees/')
            .then(function (response) {
                vm.employees = response.data.employees;
            })
    }
})
