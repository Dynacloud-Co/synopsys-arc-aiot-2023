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
