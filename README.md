# Text-to-speech Synthesizer 

## Setting up Connection to TTS Services
### Google Cloud 

1. Sign in to [Google Cloud Console](https://console.cloud.google.com/).
2. On the [project selector page](https://console.cloud.google.com/projectselector2/home/dashboard), create a new project or select an existing project. 
3. Enable billing for the selected project. 
    * For new projects, this is automatically prompted on creation of new project. 
    * For existing projects, go to the [manage billing accounts page](https://console.cloud.google.com/billing) and click on **My projects** tab. Click on the three dots under the **Actions** column and select **Change billing**. 
4. In the resources search bar located at top of page, search for Text-to-Speech API and enable it. 
5. On the [create service account page](https://console.cloud.google.com/projectselector/iam-admin/serviceaccounts/create?walkthrough_id=iam--create-service-account#step_index=1), select an existing project.
6. Fill in the service account name and service account ID. Proceed by clicking **Done**. 
7. On the [service accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts?walkthrough_id=iam--create-service-account-keys&start_index=1#step_index=1), click on the selected project.
8. Click on the email address of the service account previously created.
9. Click on the **keys** tab.
10. Click on **Add key** button and then select **Create new key**.
11. Select JSON as the key type and click **Create**. This downloads a service account key file which can be used to authenticate the service account. 

### Amazon Polly 

1. Sign in to [AWS Management Console](https://console.aws.amazon.com/) using your root account. 
2. In the search bar located at top-left of page, search for the IAM service and click on it. 
3. Under Access Management on the left, click on **Users**.
4. Click on the **Create user** button on the right hand side. Fill in the user name and click **Next**. 
5. For permissions options, select **Attach policies directly** and attach the **AmazonPollyFullAccess** policy. 
6. Click on **Security Credentials** and then **Create access key**. 
![Create access key](images/aws/create-access-key.png)
7. Select **Local code** as use case and click **Next**. Then click **Create access key** button. 
8. Go to your file explorer an navigate to your username directory (e.g. `C:\Users\USERNAME` on Windows). Check if a folder named `.aws` exists. If not, create a folder with the above name. 
9. Enter the `.aws` folder and create a file named `credentials`. 
> [!NOTE]
> Ensure that the file is named exactly as `credentials` and does not have any extensions (e.g. `credentials.txt`)
10. In the credentials file, copy and paste the three lines below.

>[default] <br />
>aws_access_key_id = YOUR_ACCESS_KEY <br />
>aws_secret_access_key = YOUR_SECRET_KEY

11. Return to the access key page. 
![Access key](images/aws/access-keys.png)

12. Copy and paste your actual access key and secret access key into the credentials file. Save the file.
![Completed credentials](images/aws/completed_credentials.png)

## Features

![User interface](images/gui/gui-v3.png)

### Select TTS Provider 
Click on the dropdown box to display TTS providers available for selection and select the desired TTS provider to be used for synthesis. 

### Select Key File
Click the **Browse** button select a valid key file as obtained from [setting up the TTS service](#google-cloud). 

> [!NOTE]
> This is only required if the TTS provider selected is Google Cloud.

### Select Mode
Click the **Text** or **SSML** button to select the desired mode. 

### Select Input File

Depending on the mode previously selected, click on the **Browse** button to select a suitable input file.

* For the Text mode, you will be prompted to select a `*.txt` file.
* For the SSML mode, you will be prompted to select a `*.ssml` file.

### Select Output Location

Click the **Browse** button to select a location to save the generated output audio file. 

### Select Language 
![Language options](images/gui/language-options.png)

Click on the dropdown box to display the languages available for selection and select the desired language to be used for synthesis. 

### Select Voice

Similarly, click on the dropdown box to display the voices available for selection and select the desired voice to be used for synthesis. 

> [!NOTE]
> Some voices available in the Text mode are not supported in the SSML mode (e.g. Chirp HD voices)

### Select Voice Engine
Similarly, click on the dropdown box to display the voice engines available for selection and select the desired voice engine to be used for synthesis. 

> [!NOTE]
> This is only supported if the TTS provider selected is Amazon Polly.

### Synthesize

Lastly, click on the **Synthesize** button to generate the output audio file. A success message will be displayed when the audio file has been successfully synthesised. 

![success message](images/gui/success-message.png)