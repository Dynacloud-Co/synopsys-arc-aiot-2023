# 2023 Synopsys ARC AIoT Design Contest 新思科技ARC盃 AIoT設計應用競賽
## Google Cloud Platform API 實作範例

* Vision (OCR)
* Text-to-Speech
* Speech-to-Text



## API Docs
### Vision (OCR)
<details>
  <summary><code>POST</code><code><b>/vision</b></code></summary>

#### Headers
> | key           | value                  | description                             |
> |---------------|------------------------|-----------------------------------------|
> | Authorization | Bearer $APP_AUTH_TOKEN | Please provide the authorization token. |

#### Parameters
> | name  |  type    | data type  | description                  |
> |-------|----------|------------|------------------------------|
> | image | required | image file | png, jpg, jpeg ... (< 10 MB) |

#### Responses
> | http code | content-type        | response            | description |
> |-----------|---------------------|---------------------|-------------|
> | `200`     | `application/json`  | `{"data": [...]}`   | OK          |
> | `4xx`     | `application/json`  | `{"errors": [...]}` | ClientError |
> | `5xx`     | `application/json`  | `{"errors": [...]}` | ServerError |

#### Example cURL
```shell
curl -X POST -k --location "$API_HOST/vision" --header "Authorization: Bearer $APP_AUTH_TOKEN" --form 'image=@"sign.jpg"'
```
</details>



### Text-to-Speech
<details>
  <summary><code>POST</code><code><b>/text-to-speech</b></code></summary>

#### Headers
> | key           | value                  | description                             |
> |---------------|------------------------|-----------------------------------------|
> | Authorization | Bearer $APP_AUTH_TOKEN | Please provide the authorization token. |

#### Parameters
> | name  |  type    | data type | description                          |
> |-------|----------|-----------|--------------------------------------|
> | text  | required | string    | Text to be converted (< 5,000 bytes) |

#### Responses
> | http code | content-type       | response            | description |
> |-----------|--------------------|---------------------|-------------|
> | `200`     | `audio/x-wav`      | audio file          | OK          |
> | `4xx`     | `application/json` | `{"errors": [...]}` | ClientError |
> | `5xx`     | `application/json` | `{"errors": [...]}` | ServerError |

#### Example cURL
```shell
curl -X POST -k --location "$API_HOST/text_to_speech" --header "Authorization: Bearer $APP_AUTH_TOKEN" --form 'text="在百家爭鳴的數位洪流時代，只要推動雲就能推動 AI 的世界。"' --output audio.wav
```
</details>



### Speech-to-Text
<details>
  <summary><code>POST</code><code><b>/speech-to-text</b></code></summary>

#### Headers
> | key           | value                  | description                             |
> |---------------|------------------------|-----------------------------------------|
> | Authorization | Bearer $APP_AUTH_TOKEN | Please provide the authorization token. |

#### Parameters
> | name  |  type    | data type  | description             |
> |-------|----------|------------|-------------------------|
> | audio | required | audio file | wav (< 1 min & < 10 MB) |

#### Responses
> | http code | content-type        | response            | description |
> |-----------|---------------------|---------------------|-------------|
> | `200`     | `application/json`  | `{"data": [...]}`   | OK          |
> | `4xx`     | `application/json`  | `{"errors": [...]}` | ClientError |
> | `5xx`     | `application/json`  | `{"errors": [...]}` | ServerError |

#### Example cURL
```shell
curl -X POST -k --location "$API_HOST/speech_to_text" --header "Authorization: Bearer $APP_AUTH_TOKEN" --form 'audio=@"audio.wav"'
```
</details>





## VM Docs
### App Information
<details>

> | Type    | Path / Command                |
> |---------|-------------------------------|
> | App Dir | /home/app/                    |
> | Config  | /home/app/dynacloud/config.py |
> | Log Dir | /var/log/app/                 |
> | Start   | `systemctl start app`         |
> | Stop    | `systemctl stop app`          |
</details>



### App Setup
<details>

#### Setup `APP_AUTH_TOKEN`
```shell
# Replace APP_AUTH_TOKEN with the random string in the config.
APP_AUTH_TOKEN=$(openssl rand -hex 40)
sed -i "s/APP_AUTH_TOKEN = '.*'/APP_AUTH_TOKEN = '$APP_AUTH_TOKEN'/" /home/app/dynacloud/config.py


# Before
APP_AUTH_TOKEN = '%_put_your_auth_token_here_%'

# After (This is an example random string. Please do not use this one.)
APP_AUTH_TOKEN = '2b417826febbb4c9cd40d0cc1f250679a3cb2d44a8ce3f93955e21218198be2e42a091dcc0b6fd38'
```



#### Enable & Start App
```shell
sudo systemctl enable app
sudo systemctl start app
sudo systemctl status app
```
</details>
