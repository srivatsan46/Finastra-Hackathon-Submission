using FinastraWeb.Models;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using Twilio;
using Twilio.Rest.Api.V2010.Account;
using Twilio.Rest.Verify.V2.Service;

using Amazon;
using Amazon.S3;
using Amazon.S3.Transfer;
using System.Threading.Tasks;
using System.IO;
using System.Web.UI.WebControls;
using System.Threading;
using MySql.Data.MySqlClient;
using Amazon.S3.Model;
using FinastraWeb.Filters;
using Amazon.S3.IO;

namespace FinastraWeb.Controllers
{
    
    public class HomeController : Controller
    {
        private readonly string accountSid = ConfigurationManager.AppSettings["ACCOUNT_ID"];
        private readonly string authToken = ConfigurationManager.AppSettings["AUTH_ID"];
        private readonly string pathServiceSid = ConfigurationManager.AppSettings["SERVICE_ID"];
        private const string bucketName = "uploadanddownloadtestfin";
        private const int duration = 12;
        private static readonly RegionEndpoint bucketRegion = RegionEndpoint.APSouth1;
        private static IAmazonS3 s3Client;      
        public static bool isUploaded = false;
        public ActionResult Index()
        {
            Session["MobileNo"] = null;
            return View();
        }

        [UserAuthenticationFilter]
        public ActionResult About()
        {            
            return View();
        }
        
        [UserAuthenticationFilter]
        [HttpPost]       
        public ActionResult UploadDocument(string documentpath)
        {
                string result = "";           
                var getmob = Session["MobileNo"];
                try
                {
                    string DocName = Path.GetFileName(documentpath);

                    s3Client = new AmazonS3Client(bucketRegion);
                    //s3Client = new AmazonS3Client(bucketRegion);
                    PutObjectRequest request = new PutObjectRequest();
                    request.BucketName = bucketName;
                    request.Key = getmob.ToString() + "_"+DocName;
                    request.FilePath = documentpath;
                    request.Metadata.Add("x-amz-meta-UserIdentifier", "+91"+getmob.ToString());
                    s3Client.PutObject(request);
                    clsDbManager db = new clsDbManager();
                    db.Open();
                    int i = db.InsertRecord_DocumentDetails(DocName, getmob.ToString());
                    db.Close();
                    if (i > 0)
                    {
                        result = "Success";
                    }
                    else
                    {
                        result = "Failed";
                    }

                }
                catch (Exception ex)
                {
                    result = ex.ToString();
                }
                        
            return Json(result, JsonRequestBehavior.AllowGet);
        }       
        static string GeneratePreSignedURL(double duration,string mobileno,string document)
        {
            string result = "";
            string urlString = "";
            try
            {
                s3Client = new AmazonS3Client(bucketRegion);
                GetPreSignedUrlRequest request = new GetPreSignedUrlRequest
                {
                    BucketName = bucketName,
                    Key = mobileno+"_"+ document,
                    Expires = DateTime.UtcNow.AddHours(duration)
                };
                urlString = s3Client.GetPreSignedURL(request);
            }
            catch (AmazonS3Exception e)
            {
                result = e.ToString();
            }
            catch (Exception e)
            {
                result = e.ToString();
            }
            return urlString;
        }
        [UserAuthenticationFilter]
        public ActionResult Dashboard()
        {
            List<UserDoc> userdoc = new List<UserDoc>();
            clsDbManager db = new clsDbManager();
            DocModel model = new DocModel();
            string result = "";
            try
            {
                db.Open();
                userdoc = db.GetDocumentDetails(Session["MobileNo"].ToString());
                UserDoc dc = new UserDoc();
                for (int i = 0; i < userdoc.Count; i++)
                {
                    string str= GeneratePreSignedURL(duration, userdoc[i].MobileNo, userdoc[i].Document);
                    userdoc[i].MobileNo = str;

                }
             
                if (userdoc != null)
                {
                    model.UserDocList = userdoc;
                }
            }
            catch (Exception ex)
            {
                result = ex.ToString(); 
            }
            return View(model);
        }
        [HttpPost]
        public ActionResult GetOtp(string mobile_number,string mode)
        {
            string status = "";            
            try
            {
                if (mode == "Reg")
                {
                    clsDbManager dbmgr = new clsDbManager();
                    dbmgr.Open();
                    bool isreg = dbmgr.IsReg(mobile_number);
                    dbmgr.Close();
                    if (isreg == true)
                    {
                        status = "registered";
                    }
                    else
                    {
                        TwilioClient.Init(accountSid, authToken);
                        var verification = VerificationResource.Create(
                            to: "+91" + mobile_number,
                            channel: "sms",
                            pathServiceSid: pathServiceSid
                            );
                        status = verification.Status;
                    }
                }
                else
                {
                    clsDbManager dbmgr = new clsDbManager();
                    dbmgr.Open();
                    bool isreg = dbmgr.IsReg(mobile_number);
                    dbmgr.Close();
                    if (isreg == true)
                    {
                        TwilioClient.Init(accountSid, authToken);
                        var verification = VerificationResource.Create(
                            to: "+91" + mobile_number,
                            channel: "sms",
                            pathServiceSid: pathServiceSid
                            );
                        status = verification.Status;
                    }
                    else
                    {
                        status = "Notregistered";
                    }
                }

            }
            catch (Exception ex)
            {
                status = "Error";
            }
            return Json(status, JsonRequestBehavior.AllowGet);
        }
        
        [HttpPost]
        public ActionResult VerifyOtp(string mobileNo,string code)
        {
            string status = "";
            try
            {
                TwilioClient.Init(accountSid, authToken);

                var verificationCheck = VerificationCheckResource.Create(
                to: "+91" + mobileNo,
                code: code,
                pathServiceSid: pathServiceSid
                );
                status = verificationCheck.Status;

                if (status == "approved")
                {
                    clsDbManager dbmgr = new clsDbManager();
                    dbmgr.Open();
                    int i = dbmgr.InsertRecord_UserDetails(mobileNo, "sa");
                    dbmgr.Close();
                    Session["MobileNo"] = mobileNo;
                }

            }            
            catch (Exception ex)
            {
                if (ex.Message == "Invalid parameter: Code")
                {
                    status = "400";
                }
                else 
                {
                    status = "Error";
                }              

            }
            return Json(status, JsonRequestBehavior.AllowGet);
        }
        public ActionResult Registration()
        {
            return View();
        }
        public ActionResult LogOut()
        {
            Session["MobileNo"] = null;
            return RedirectToAction("Index");
        }
        public ActionResult Share()

        {

            return View();

        }


    }
}