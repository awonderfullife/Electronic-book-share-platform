function UserManager() {
    var self = this;
    self.loginHooks = [];
    self.logoutHooks = [];
    self.login = function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            type: 'POST',
            url: '/login',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                console.log(data);
                self.getUser();
                $('#myModal').modal('hide');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                $('#login-error').removeClass('hidden');
            }
        });
    };
    self.logout = function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/logout',
            contentType: false,
            processData: false,
            success: function(data) {
                console.log(data);
                $.each(self.logoutHooks, function(index, hook) {
                    hook();
                });
            },
            error: function(jqXHR, textStatus, errorThrown) {
            }
        });
    };
    self.getUser = function() {
        $.ajax({
            type: 'GET',
            url: '/api/v1/user',
            success: function(data) {
                console.log(data);
                $.each(self.loginHooks, function(index, hook) {
                    hook(data);
                });
            },
            error: function(jqXHR, textStatus, errorThrown) {
                $('#nav-login').removeClass('hidden');
                console.log(jqXHR.status);
            }
        });
    };
    self.addLoginHook = function(hook) {
        self.loginHooks.push(hook);
    };
    self.addLogoutHook = function(hook) {
        self.logoutHooks.push(hook);
    };
    self.run = self.getUser;
}

var userManager = new UserManager();

userManager.addLoginHook(function(user) {
    $('#username').html(user.username + " <span class='caret'></span>");
    $('#nav-username').removeClass('hidden');
    $('#nav-login').addClass('hidden');
});

userManager.addLogoutHook(function() {
    $('#username').html("");
    $('#nav-username').addClass('hidden');
    $('#nav-login').removeClass('hidden');
    window.location.href='/';
});

$('#login-form').on('submit', userManager.login);
$('#logout').click(userManager.logout);
