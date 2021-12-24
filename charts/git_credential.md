git 登入免帳號密碼並加密
--
* 請確認執行過[加密docker login 密碼on ubuntu 18.04](docker_pass.md)
* 以下所有的動作都是在$HOME底下執行，如你再不同的目錄執行，請依據自己的情況修正
1. 取得gpg key
    ```bash
    gpg -k 
    /home/neocyc/.gnupg/pubring.kbx
    -------------------------------
    pub   rsa4096 2019-12-23 [SC]
          D6B88C72BC0A50000XXXXA9BED1DB860CD67A00X
    uid           [ultimate] neochang <eric228@gmail.com>
    sub   rsa4096 2019-12-23 [E]
    ```
2. 新增檔案credentials
    ```bash
    machine gitlab.nexuera.com
    login <user-name>
    password <password>
    protocol https
    ```
    多個git server設定時只要對應的增加即可
    ```bash
    machine gitlab.nexuera.com
    login <user-name>
    password <password>
    protocol https
 
    machine github.com
    login <user-name>
    password <password>
    protocol https
    ```
3. 用剛剛的gpg id來加密檔案
    ```bash
    gpg -r D6B88C72BC0A50000XXXXA9BED1DB860CD67A00X --encrypt --trust-model always credentials
    ```
4. 這時你應該會看到credentials.gpg這個檔案，然後可以刪除掉credentials
5. /usr/local/bin/credential-helper.sh 用來將加密過後的帳號密碼解密，並傳給git．因此請注意cerdentials
.gpg請放在$HOME底下
    ```bash
    #!/usr/bin/env bash
    git-credential-netrc -f $HOME/credentials.gpg get
    # 如果你不是放在$HOME底下，請修改到正確的位置
    ```
6. 設定git credentials helper
    ```bash
    git config --global credential.helper /usr/local/bin/credential-helper
    ```

到此已經完成設定，可以使用加密過的帳號密碼來進行git操作了
