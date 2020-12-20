using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Linq;
using System.Web;

namespace FinastraWeb.Models
{
    public class clsDbManager
    {
        public MySqlConnection con;
        MySqlCommand cmd;
        public void Open()
        {
            string constr = "Data Source=" + ConfigurationManager.AppSettings["HOSTNAME"] + ";Initial Catalog=" + ConfigurationManager.AppSettings["DATABASE"] + ";User ID=" + ConfigurationManager.AppSettings["USERNAME"] + ";Password=" + ConfigurationManager.AppSettings["PASSWORD"] + ";";
            con = new MySqlConnection(constr);
            con.Open();            
        }
        public void Close()
        {
            con.Close();
        }
        public int InsertRecord_UserDetails(string mobno, string username)
        {
            int u = 0;

            try
            {
                string str = "Insert Into UserDetails(MobileNo,UserName) values('" + mobno + "','" + username + "')";
                cmd = new MySqlCommand(str, con);
                u = cmd.ExecuteNonQuery();
                return u;
            }
            catch (Exception Ex)
            { }
            return u;
        }
        public bool IsReg(string mobno)
        {
            bool reg = false;
            try
            {
                string str = "Select COUNT(*) from UserDetails where MobileNo='" + mobno + "'";
                cmd = new MySqlCommand(str, con);
                MySqlDataReader dr = cmd.ExecuteReader();                
                if (dr.Read())
                {
                    int i = Convert.ToInt32(dr[0]);
                    if (i > 0)
                    {
                        reg = true;
                    }
                }
                dr.Close();

                return reg;
            }
            catch (Exception ex)
            {

            }
            return reg;
        }
        public int InsertRecord_DocumentDetails(string docname, string mobileno)
        {
            int u = 0;

            try
            {
                string str = "Insert Into UserDocumentDetails(DocName,MobileNo) values('" + docname + "','" + mobileno + "')";
                cmd = new MySqlCommand(str, con);
                u = cmd.ExecuteNonQuery();
                return u;
            }
            catch (Exception Ex)
            { }
            return u;
        }
        public List<UserDoc> GetDocumentDetails(string mobileno)
        {
            List<UserDoc> doc = new List<UserDoc>();
            UserDoc dc;
            try
            {
                string str = "Select Id,DocName,MobileNo from UserDocumentDetails where MobileNo='" + mobileno + "'";
                cmd = new MySqlCommand(str, con);
                MySqlDataReader dr = cmd.ExecuteReader();
                while (dr.Read())
                {
                    dc = new UserDoc();
                    dc.Id= Convert.ToInt32(dr["Id"]);
                    dc.Document = Convert.ToString(dr["DocName"]);
                    dc.MobileNo = Convert.ToString(dr["MobileNo"]);
                    doc.Add(dc);
                }
                dr.Close();              
            }
            catch (Exception ex)
            {

            }
            return doc;
        }


    }
}