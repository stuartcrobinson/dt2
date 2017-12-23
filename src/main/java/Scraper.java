import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.w3c.dom.Document;
import org.w3c.dom.Node;

import java.io.File;
import java.io.IOException;

import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

public class Scraper {
  static XPath xPath = XPathFactory.newInstance().newXPath();


  public static void main(String[] asdf) throws IOException, InterruptedException, XPathExpressionException {

    System.setProperty("webdriver.chrome.driver", new File(".").getCanonicalPath() + "/chromedriver_2.34");

    WebDriver driver = new ChromeDriver();

    for (int year = 1979; year < 2019; year++) {
      String url = getUrl(year);

      String text = getNobelTextFromChromeDriver(url, driver);
//      String text = getNobelTextFromDoc(url);

      if (text.contains(", Ladies and Gentlemen")) {
        text = text.split(", Ladies and Gentlemen")[1];
      }
      if (text.contains(" Excellencies, Ladies and gentlemen")) {
        text = text.split(" Excellencies, Ladies and gentlemen")[1];
      }
      if (text.contains(" Excellencies, ladies and gentlemen")) {
        text = text.split(" Excellencies, ladies and gentlemen")[1];
      }
      if (text.contains("Presentation Speech by")) {
        text = text.split("Presentation Speech by")[1];
      }
      text = text.split("From Nobel Lectures,")[0];
      text = text.split("Share this:")[0];
      text = text.split("Copyright © The Nobel Foundation")[0];

//      System.out.println(url);
      System.out.println(text);
      System.out.println("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------");
      System.out.println("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------");
      System.out.println("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------");
    }
  }

  private static String getNobelTextFromChromeDriver(String url, WebDriver driver) {

    driver.get(url);
//    <span itemscope="" itemtype="http://schema.org/Person">
    String text = driver.findElement(By.xpath("//div[@class='large-12 columns']//span[@itemscope and @itemtype]")).getText();

    return text;
  }

  private static String getNobelTextFromDoc(String url) throws IOException, InterruptedException, XPathExpressionException {

    Document doc = HttpDownloadUtility.getWebpageDocument(url);

    Node aElement = (Node) xPath.evaluate("//div[@class='large-12 columns']//span[@itemscope and @itemtype]", doc, XPathConstants.NODE);

    return aElement.getTextContent();
  }

  private static String getUrl(int year) {
    String DATEGOESHERE = "DATEGOESHERE";
    String baseUrl = "https://www.nobelprize.org/nobel_prizes/peace/laureates/DATEGOESHERE/presentation-speech.html";
    return baseUrl.replace(DATEGOESHERE, year + "");
  }
}
