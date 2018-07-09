var mailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
            var mails = model.toEmails.split(";")
            for (let i = 0; i < mails.length; i++) {
                if (!mailReg.test(mails[i])) {
                    toastr.error("收件人格式错误！")
                    flag = false;
                    break;
                }
            }
