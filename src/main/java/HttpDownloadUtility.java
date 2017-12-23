import org.apache.commons.io.IOUtils;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.message.BasicHeader;
import org.htmlcleaner.CleanerProperties;
import org.htmlcleaner.DomSerializer;
import org.htmlcleaner.HtmlCleaner;
import org.htmlcleaner.TagNode;
import org.w3c.dom.Document;
import org.xml.sax.InputSource;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

/**
 * A utility that downloads a file from a URL.
 * <p>
 * originally from  www.codejava.net
 */
public class HttpDownloadUtility {

  private static final int BUFFER_SIZE = 4096;

  public static List<String> getFile(String urlStr) throws IOException, InterruptedException {

    List<String> lines = new ArrayList();

    try (BufferedReader br = new BufferedReader(new InputStreamReader(getWebInputStream(urlStr)))) {
      String line;
      while ((line = br.readLine()) != null)
        lines.add(line);
    }
    return lines;
  }

  public static String getFileSt(String fileURL) throws IOException, InterruptedException {

    List<String> lines = getFile(fileURL);

    StringBuilder sb = new StringBuilder();

    for (String line : lines)
      sb.append(line).append(System.lineSeparator());

    return sb.toString();
  }

  /**
   * is persistent by default
   */
  public static void downloadFile(String urlStr, File file) throws IOException, InterruptedException {
    InputStream is = getWebInputStream(urlStr, true);
    downloadFile(is, file);
  }

  public static void downloadFile(String urlStr, File file, Boolean be_persistent) throws IOException, InterruptedException {
    InputStream is = getWebInputStream(urlStr, be_persistent);
    System.out.println(urlStr);
    downloadFile(is, file);
  }

  public static void downloadFile(InputStream is, File file) throws IOException, InterruptedException {

    try (FileOutputStream outputStream = new FileOutputStream(file)) {
      int bytesRead;
      byte[] buffer = new byte[BUFFER_SIZE];
      while ((bytesRead = is.read(buffer)) != -1) {
        System.out.println(buffer);
        outputStream.write(buffer, 0, bytesRead);
      }
      System.out.print(" - " + file.getName() + " downloaded");
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  /**
   * persistent by default
   */
  static InputStream getWebInputStream(String urlSt) throws IOException, PermissionDeniedWebException, InterruptedException {
    return getWebInputStream(urlSt, true);
  }

  /**
   * ONLY use this for web access.  DO NOT access web in any other way! except selenium
   */
  static InputStream getWebInputStream(String urlSt, Boolean be_persistent) throws IOException, PermissionDeniedWebException, Bad_Gateway_Exception, InterruptedException {

    URL url;
    url = new URL(urlSt);
    InputStream is;

    try {
      HttpURLConnection httpConn = (HttpURLConnection) url.openConnection();
      httpConn.setConnectTimeout(40_000);
      httpConn.setReadTimeout(40_000);
      is = httpConn.getInputStream();
    } catch (IOException e) {
      System.out.println("first exception for:\n" + urlSt);
      if (e.toString().contains("code: 500 for URL"))
        throw new PermissionDeniedWebException(e.toString());
      if (e.toString().contains("code: 502 for URL"))
        throw new Bad_Gateway_Exception(e.toString());
      if (!be_persistent) {
        throw e;
      } else {
        try {
          System.out.println("failed to load page. try again in 1 seconds..." + urlSt);
          Thread.sleep(1000);
          HttpURLConnection httpConn = (HttpURLConnection) url.openConnection();
          is = httpConn.getInputStream();
          System.out.println("it worked the 2nd time! " + urlSt);
        } catch (IOException e2) {
          System.out.println("failed 2nd time. try again in 4 seconds..." + urlSt);
          Thread.sleep(4000);
          HttpURLConnection httpConn = (HttpURLConnection) url.openConnection();
          try {
            is = httpConn.getInputStream();
            System.out.println("it worked the 3rd time! " + urlSt);
          } catch (Exception e3) {
            System.out.println("failed the 3rd time. giving up " + urlSt);
            throw e3;
          }
        }
      }
    }
    return is;
  }

  /**
   * cascading try's cos once IOUtils threw a java.net.SocketTimeoutException
   */
  public static String getPageSource(String urlStr) throws InterruptedException, PermissionDeniedWebException, IOException {
    return getPageSource(urlStr, true);
  }

  /**
   * cascading try's cos once IOUtils threw a java.net.SocketTimeoutException
   */
  public static String getPageSource(String urlStr, boolean persistance) throws InterruptedException, PermissionDeniedWebException, IOException {

    try {
      return IOUtils.toString(getWebInputStream(urlStr, persistance));
    } catch (PermissionDeniedWebException pdex) {
      throw pdex;
    } catch (IOException ex) {
      try {
        return IOUtils.toString(getWebInputStream(urlStr, persistance));
      } catch (IOException ex1) {
        return IOUtils.toString(getWebInputStream(urlStr, persistance));
      }
    }
  }

  public static Document loadXMLFromString(String xml) throws Exception {
    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    DocumentBuilder builder = factory.newDocumentBuilder();
    InputSource is = new InputSource(new StringReader(xml));
    return builder.parse(is);
  }

  public static Document getWebpageDocument(String urlStr) throws InterruptedException, IOException {
    try {
      HtmlCleaner cleaner = new HtmlCleaner();
      CleanerProperties props = cleaner.getProperties();
      props.setAllowHtmlInsideAttributes(true);
      props.setAllowMultiWordAttributes(true);
      props.setRecognizeUnicodeChars(true);
      props.setOmitComments(true);

      DocumentBuilderFactory builderFactory = DocumentBuilderFactory.newInstance();
      DocumentBuilder builder = null;
      try {
        builder = builderFactory.newDocumentBuilder();
      } catch (ParserConfigurationException e) {
        e.printStackTrace();
      }
      String source = HttpDownloadUtility.getPageSource(urlStr);

      TagNode tagNode = new HtmlCleaner().clean(source);

      Document doc = new DomSerializer(new CleanerProperties()).createDOM(tagNode);

      return doc;
    } catch (ParserConfigurationException ex) {
      ex.printStackTrace();
      return null;
    }
  }

  public static Document getWebpageDocument_fromSource(String source) throws InterruptedException, IOException {
    try {
      HtmlCleaner cleaner = new HtmlCleaner();
      CleanerProperties props = cleaner.getProperties();  //might not be necessary
      props.setAllowHtmlInsideAttributes(true);
      props.setAllowMultiWordAttributes(true);
      props.setRecognizeUnicodeChars(true);
      props.setOmitComments(true);

      TagNode tagNode = new HtmlCleaner().clean(source);

//            System.out.println(source);
//            System.out.println(tagNode.getAllElementsList(true));

      Document doc = new DomSerializer(props).createDOM(tagNode);
//            System.out.println(doc.toString());

      return doc;
    } catch (ParserConfigurationException ex) {
      ex.printStackTrace();
      return null;
    }
  }

  public static String getRequest(String url, BasicHeader... headers) throws IOException {

    HttpClient httpClient = HttpClientBuilder.create().build();
    HttpGet request = new HttpGet(url);
    for (BasicHeader header : headers)
      request.addHeader(header.getName(), header.getValue());
    HttpResponse response = httpClient.execute(request);
    String responseString = new BasicResponseHandler().handleResponse(response);
    StatusLine statusLine = response.getStatusLine();
//        String responses = response.toString() + System.lineSeparator() + responseString + System.lineSeparator();
//
////        System.out.print(responses);
//        System.out.print(responseString);
//        System.out.println();

    if (statusLine.getStatusCode() != 200) {
      throw new RuntimeException("Http status is not 200. Status line:" + statusLine.toString());
    }
    return responseString;
  }

  public static class PermissionDeniedWebException extends IOException {
    public PermissionDeniedWebException(String toString) {
    }
  }

  /**
   * http error 502.   http://www.checkupdown.com/status/E502.html <br><br> This usually does not mean that the upstream server is down (no response to the gateway/proxy), but rather that the upstream server and the gateway/proxy do not agree on the protocol for exchanging data. Given that Internet protocols are quite clear, it often means that one or both machines have been incorrectly or incompletely programmed.
   */
  public static class Bad_Gateway_Exception extends IOException {
    public Bad_Gateway_Exception(String toString) {
    }
  }


  /**
   * Downloads a file from a URL
   *
   * @param fileURL HTTP URL of the file to be downloaded
   * @param saveDir path of the directory to save the file
   * @throws IOException
   */
  public static void downloadFile3(String fileURL, String saveDir) throws IOException {
    URL url = new URL(fileURL);
    HttpURLConnection httpConn = (HttpURLConnection) url.openConnection();
    int responseCode = httpConn.getResponseCode();

    // always check HTTP response code first
    if (responseCode == HttpURLConnection.HTTP_OK || true) {
      String fileName = "";
      String disposition = httpConn.getHeaderField("Content-Disposition");
      String contentType = httpConn.getContentType();
      int contentLength = httpConn.getContentLength();

      if (disposition != null) {
        // extracts file name from header field
        int index = disposition.indexOf("filename=");
        if (index > 0) {
          fileName = disposition.substring(index + 10,
                                           disposition.length() - 1);
        }
      } else {
        // extracts file name from URL
//                fileName = fileURL.substring(fileURL.lastIndexOf("/") + 1,
//                        fileURL.length());
        fileName = "hi.txt";
      }

      System.out.println("Content-Type = " + contentType);
      System.out.println("Content-Disposition = " + disposition);
      System.out.println("Content-Length = " + contentLength);
      System.out.println("fileName = " + fileName);

      // opens input stream from the HTTP connection
      InputStream inputStream = httpConn.getInputStream();
      String saveFilePath = saveDir + File.separator + fileName;

      // opens an output stream to save into file
      FileOutputStream outputStream = new FileOutputStream(saveFilePath);

      int bytesRead = -1;
      byte[] buffer = new byte[BUFFER_SIZE];
      while ((bytesRead = inputStream.read(buffer)) != -1) {
        outputStream.write(buffer, 0, bytesRead);
      }

      outputStream.close();
      inputStream.close();

      System.out.println("File downloaded");
    } else {
      System.out.println("No file to download. Server replied HTTP code: " + responseCode);
    }
    httpConn.disconnect();
  }


}
