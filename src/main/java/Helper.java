import com.google.common.base.CharMatcher;

import org.htmlcleaner.CleanerProperties;
import org.htmlcleaner.DomSerializer;
import org.htmlcleaner.HtmlCleaner;
import org.htmlcleaner.TagNode;
import org.unbescape.html.HtmlEscape;
import org.w3c.dom.Document;

import java.io.IOException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

public class Helper {


    public static String cleanText(String text) {

        text = HtmlEscape.unescapeHtml(text).toLowerCase().trim();
        text = CharMatcher.WHITESPACE.and(CharMatcher.isNot(' ')).removeFrom(text);
        text = text.trim();
        return text;
    }

    public static Document getWebpageDocument_fromSource(String source) throws InterruptedException, IOException {
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

            TagNode tagNode = new HtmlCleaner().clean(source);

            Document doc = new DomSerializer(new CleanerProperties()).createDOM(tagNode);

            return doc;
        } catch (ParserConfigurationException ex) {
            ex.printStackTrace();
            return null;
        }
    }
}
