class Translation(object):
    ctry_lst = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla',
                'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan',
                'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda',
                'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina',
                'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria',
                'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands',
                'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands',
                'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica',
                "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti',
                'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea',
                'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France',
                'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany',
                'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey',
                'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands',
                'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia',
                'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan',
                'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of",
                'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon',
                'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao',
                'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta',
                'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
                'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat',
                'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia',
                'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands',
                'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea',
                'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion',
                'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy',
                'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia',
                'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa',
                'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone',
                'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia',
                'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname',
                'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic',
                'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste',
                'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
                'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
                'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu',
                'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.',
                'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
    START_TEXT = """မင်္ဂလာပါ ♥ {},
꧁༒༺ FDMN Channel မှ ကြိုဆိုပါတယ် ༻༒꧂
/help ꜰᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟꜱ!"""
    FORMAT_SELECTION = "Select the desired format: <a href='{}'>file size might be approximate</a> \nIf you want to set custom thumbnail, send photo before or quickly after tapping on any of the below buttons.\nYou can use /deletethumbnail to delete the auto-generated thumbnail."
    SET_CUSTOM_USERNAME_PASSWORD = """If you want to download premium videos, provide in the following format:
URL | filename | username | password"""
    DOWNLOAD_START = "Now Downloading.."
    UPLOAD_START = "Now Uploading.."
    RCHD_TG_API_LIMIT = "Downloaded in {} seconds.\nDetected File Size: {}\nSorry. But, I cannot upload files greater than 2GB due to Telegram API limitations."
    AFTER_SUCCESSFUL_UPLOAD_MSG = "Thanks for using @GroupDcBots)"
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "Downloaded in {} seconds.\nUploaded in {} seconds.\n\n@Film_Day_Bot"
    SAVED_CUSTOM_THUMB_NAIL = "Custom video / file thumbnail saved. This image will be used in the video / file."
    DEL_ETED_CUSTOM_THUMB_NAIL = "✅ Custom thumbnail cleared succesfully."
    CUSTOM_CAPTION_UL_FILE = "{}"
    NO_VOID_FORMAT_FOUND = "ERROR...\n<b>YouTubeDL</b> said: {}"
    HELP_USER = """How to Use Me? Follow These steps!
    
1. Send url (example.domain/File.mp4 | New Filename.mp4).
2. Send Image As Custom Thumbnail (Optional).
3. Select the button.
   SVideo - Give File as video with Thumbnail
   SFile  - Give File (video) as file with Thumbnail
   Video  - Give File as video without Thumbnail
   File   - Give File without Thumbnail
   
   Channel  => t.me/fdmnchannel
   Group    => t.me/fdmnchat
   Transloader Bot => @GTransLoaderbot
   Tansloader Site => t.me/transload"""
    REPLY_TO_DOC_GET_LINK = "Reply to a Telegram media to get High Speed Direct Download Link"
    REPLY_TO_DOC_FOR_C2V = "Reply to a Telegram media to convert"
    REPLY_TO_MEDIA_ALBUM_TO_GEN_THUMB = "Reply /genthumbnail to a media album, to generate custom thumbnail"
    ERR_ONLY_TWO_MEDIA_IN_ALBUM = "Media Album should contain only two photos. Please re-send the media album, and then try again, or send only two photos in an album."
    CANCEL_STR = "Process Cancelled"
    ZIP_UPLOADED_STR = "Uploaded {} files in {} seconds"
    SLOW_URL_DECED = "Gosh that seems to be a very slow URL. Please find another source."
    DOWNLOAD_FILE = " 📥Downloading File📥"
    UPLOAD_FILE = " 📤Uploading📤 \n\n To  transfer.sh "
    REPLY_TO_DOC_FOR_RENAME_FILE = "Reply to a Telegram media to /ren with custom thumbnail support"
    CUSTOM_CAPTION_UL_FILE = " "
    FILE_NOT_FOUND = "Error, File not Found!!"
    RENAME_403_ERR = "Sorry. You are not permitted to rename this file."
    SAVED_RECVD_DOC_FILE = "Document Downloaded Successfully."
    AFTER_GET_DL_LINK = " <b>File Name :</b> <code>{}</code>\n<b>File Size :</b> {}\n\n<b>⚡Link⚡ :</b> <code>{}</code>\n\nValid for <b>14</b> days.\nJoin : https://t.me/fdmnchannel"
    EXTRACT_ZIP_INTRO_ONE = "Send a compressed file first, Then reply /unzip command to the file."
    EXTRACT_ZIP_INTRO_THREE = "Analyzing received file. ⚠️ This might take some time. Please be patient. "
    UNZIP_SUPPORTED_EXTENSIONS = ("zip", "rar")
    EXTRACT_ZIP_ERRS_OCCURED = "Sorry. Errors occurred while processing compressed file. Please check everything again twice, and if the issue persists, report this to <a href='https://t.me/fdmnchat</a>"
    EXTRACT_ZIP_STEP_TWO = "Select file_name to upload from the below options."
    #CHNL_JOIN = "အသစ်ရောက်လာတဲ့သူတွေက 'ဇာတ်လမ်းကြည့်ရန် နှိပ်ပါ' ကို မနှိပ်ခင် 'Channel Join ရန် နှိပ်ပါ' ကို အရင်နှိပ်ပြီး Private Channel ပေါ်လာရင် Join Channel ကိုနှိပ်ပါ။\nတစ်ကြိမ်လုပ်ဆောင်ပြီးသွားရင် 'ဇာတ်လမ်းကြည့်ရန် နှိပ်ပါ' ကနေတန်းကြည့်နိုင်ပါပြီ။\nPrivate Channel တစ်ခုထက်မကရှိတာမို့ သေချာအောင် Join Channel အရင်လုပ်စေချင်ပါတယ်။\nဇာတ်လမ်းအသစ်ကို Facebook Newfeeds ကနေစောင့်ကြည့်နိုင်ဖို့ 👉<a href='https://www.facebook.com/fdmntelegram'>FDMN Facebook Page</a>👈 ကို Like-Follow-Share လေးလုပ်ထားနိုင်ပါတယ်။"
    #CHNL_JOIN = "အသစ်ရောက်လာတဲ့သူတွေက...\n\nအဆင့် (၁) - 'Channel Join ရန် နှိပ်ပါ' ကို နှိပ်ပါ။ 'Welcome to FDMN' Bot ထဲ ရောက်သွားပါလိမ့်မယ်။\n\nအဆင့် (၂) - Bot ထဲရောက်သွားရင် Start သို့မဟုတ် Restart ကိုနှိပ်ပြီး လမ်းညွှန်ချက်အတိုင်း လုပ်ဆောင်ပါ။ '/start' လို့ စာရိုက်ပို့လည်းရပါတယ်။\n\nအဆင့် (၃) - Channel လေးတွေပေါ်လာရင် Join ချင်တဲ့ Channelကို နှိပ်ပြီး 'Join' သို့မဟုတ် 'Join Channel' ကို နှိပ်ပါ။\n\n<b>တစ်ကြိမ်လုပ်ဆောင်ပြီးသွားရင် 'ဇာတ်လမ်းကြည့်ရန် နှိပ်ပါ' ကနေတန်းကြည့်နိုင်ပါပြီ။</b>\n\nJoin နိုင်တဲ့ လက်ရှိ Private Channel များ...\n(၁) ရုပ်ရှင်စုံလင်\n(၂) Bollywood/Tallywood ဇာတ်လမ်းများ\n(၃) ကာတွန်းဇာတ်လမ်းများ\n(၄) 18+ ဇာတ်လမ်းများ\n\nဇာတ်လမ်းအသစ်ကို Facebook Newfeeds ကနေစောင့်ကြည့်နိုင်ဖို့ 👉<a href='https://www.facebook.com/fdmntelegram'>FDMN Facebook Page</a>👈 ကို Like-Follow-Share လေးလုပ်ထားနိုင်ပါတယ်။"
    CHNL_FB = "ဇာတ်လမ်းအသစ်ကို Facebook Newfeeds ကနေစောင့်ကြည့်နိုင်ဖို့ 👉<a href='https://www.facebook.com/fdmntelegram'>FDMN Facebook Page</a>👈 ကို Like-Follow-Share လေးလုပ်ထားနိုင်ပါတယ်။"
    #CHNL_JOIN = "<b>အသစ်ရောက်လာတဲ့သူတွေက...</b>\n<b>Private Channel တွေထဲဝင်နည်း Video ကို 👉<a href='https://t.me/fdmnchannel/783'> ဒီနေရာမှာ</a>👈 နှိပ်ပြီး ကြည့်ပါ။</b>\n<b>Video ထဲကအတိုင်း တစ်ကြိမ်လုပ်ဆောင်ပြီးသွားရင် 'ဇာတ်လမ်းကြည့်ရန် နှိပ်ပါ' ကနေတန်းကြည့်နိုင်ပါပြီ။\nဝင်ကြေးပေးစရာမလို(အခမဲ့)ပါ။</b>\n\nJoin နိုင်တဲ့ လက်ရှိ Private Channel များ...\n(၁) ရုပ်ရှင်စုံလင်\n(၂) Bollywood/Tallywood ဇာတ်လမ်းများ\n(၃) ကာတွန်းဇာတ်လမ်းများ\n(၄) 18+ ဇာတ်လမ်းများ\n\nဇာတ်လမ်းအသစ်ကို Facebook Newfeeds ကနေစောင့်ကြည့်နိုင်ဖို့ 👉<a href='https://www.facebook.com/fdmntelegram'>FDMN Facebook Page</a>👈 ကို Like-Follow-Share လေးလုပ်ထားနိုင်ပါတယ်။"
    CHNL_JOIN = '''<b>မန်ဘာမဝင်ရသေးပါက</b> 👇
မန်ဘာကြေး ကျပ် ၈၀၀ သို့မဟုတ် ဘတ် ၁၀ တည်းနဲ့
FDMN ကတင်ဆက်တဲ့ Series Movies အားလုံးကို ကြည့်ရှုနိုင်ပါတယ်။
မန်ဘာဝင်ရန် 👉<a href='https://t.me/FDMN_Signup_Bot'> ဒီကို</a>👈 သွားပြီး
START သို့မဟုတ် RESTART ကိုနှိပ်ပါ၊ "/start" လို့ရိုက်ပို့လည်းရပါတယ်။
ပြီးလျှင် ပေါ်လာတဲ့ လမ်းညွှန်ချက်အတိုင်းလုပ်ဆောင်ပါ။

<b>မန်ဘာဝင်ပြီးပါက</b> 👇
Private Channel တွေထဲဝင်နည်း Video ကို 👉<a href='https://t.me/fdmnchannel/4430'> ဒီနေရာမှာ</a>👈 နှိပ်ပြီး ကြည့်ပါ။</b>
Video ထဲကအတိုင်း တစ်ကြိမ်လုပ်ဆောင်ပြီးသွားရင် 'ဇာတ်လမ်းကြည့်ရန် နှိပ်ပါ' ကနေတန်းကြည့်နိုင်ပါပြီ။

ဇာတ်လမ်းအသစ်ကို Facebook Newfeeds ကနေစောင့်ကြည့်နိုင်ဖို့ 👉<a href='https://www.facebook.com/fdmntelegram'>FDMN Facebook Page</a>👈 ကို Like-Follow-Share လေးလုပ်ထားနိုင်ပါတယ်။'''
