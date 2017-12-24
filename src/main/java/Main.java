import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

//how to save?
//save as three files.
// 1.  list of all frags
// 2.  list of indices of frags making up the original text.
//xTODO - done - not coding whole words properly.  "but" is a frag that's used internally, but single word gets split into letters. same as "are" and "is"

//xTODO - no - add anohter cap character that means all-caps.  instead of capping letters individually.

//TODO - experiment with text generation using embedding vs fragged.  so save a file for this.  create caps char for whole word caps.

//TODO - output and load into lstm in python!
/*
TODO make 4 files:
1. wholeWords
2. frags
3. wholeWordIndices
4. fragIndices

1 and 2 are a compound per line.  line number - 1 is index for that word/compound/char
 */
public class Main {
  public static PrintStream o = System.out;


  public static int maxFragSize = 4;
  public static double minQuality = 1;

  public static void out(Object x) {
    System.out.println(x);
  }

  public static Map<String, Integer> m_prefix_count = new HashMap<>();
  public static Map<String, Integer> m_suffix_count = new HashMap<>();
  public static Map<String, Integer> m_wholeWord_count = new HashMap<>();
  public static Map<Integer, Integer> m_prefixLen_count = new HashMap<>();
  public static Map<Integer, Integer> m_suffixLen_count = new HashMap<>();
  public static Map<Integer, Integer> m_wholeWordLen_count = new HashMap<>();
  public static Map<String, Double> m_prefix_q = new HashMap<>();
  public static Map<String, Double> m_suffix_q = new HashMap<>();
  public static Map<String, Double> m_wholeWord_q = new HashMap<>();


  //https://stackoverflow.com/questions/2206378/how-to-split-a-string-but-also-keep-the-delimiters
  public static void main(String[] adsf) throws IOException {

    String[] ar = getArrayOfCompoundsSplitBeforeSpaceAndPunctuation(new File("./src/main/resources/nobelPeaceSince79.txt"));

    fillCountsMaps(ar);
    fillLenCountsMaps();

    displayCountsMaps();

    fillQualitiesMaps();

//    System.exit(0);

    List<SegmentingWord> words = convertArrayToProcessedWords(ar);

    Set<String> allFrags = new HashSet<>();
    Set<String> allWholeWords = new HashSet<>();

    for (SegmentingWord word : words) {
      List<String> finalForm = word.getFinalForm();
      List<String> finalWholeWordForm = word.getWholeWordFinalForm();
//      out(" " + word.originalWord);
//      out(finalForm);
//      out(finalWholeWordForm);

      allFrags.addAll(finalForm);
      allWholeWords.addAll(finalWholeWordForm);
    }

    //now print results to file
    /*
1. wholeWords
2. frags
3. wholeWordIndices
4. fragIndices
*/
    List<String> fragsUnique = new ArrayList<>(allFrags);
    Collections.sort(fragsUnique);
    List<String> wholeWordsUnique = new ArrayList<>(allWholeWords);
    Collections.sort(wholeWordsUnique);

    Map<String, Integer> m_frag_index = new HashMap<>();
    Map<String, Integer> m_word_index = new HashMap<>();

    for (int i = 0; i < fragsUnique.size(); i++) {
      m_frag_index.put(fragsUnique.get(i), i);
    }
    for (int i = 0; i < wholeWordsUnique.size(); i++) {
      m_word_index.put(wholeWordsUnique.get(i), i);
    }
    List<Integer> inputFragEncoded = new ArrayList<>();
    List<Integer> inputWordEncoded = new ArrayList<>();

    for (SegmentingWord word : words) {
      List<String> finalForm = word.getFinalForm();
      List<String> finalWholeWordForm = word.getWholeWordFinalForm();

      for (String frag : finalForm) {
        inputFragEncoded.add(m_frag_index.get(frag));
      }
      for (String wholeWord : finalWholeWordForm) {
        inputWordEncoded.add(m_word_index.get(wholeWord));
      }
    }
    new File("output").mkdirs();

    Files.write(new File("output/fragsUnique.txt").toPath(), fragsUnique);
    Files.write(new File("output/wholeWordsUnique.txt").toPath(), wholeWordsUnique);
    Files.write(new File("output/fragIndices.txt").toPath(), inputFragEncoded.stream().map(i -> i.toString()).collect(Collectors.toList()));
    Files.write(new File("output/wholeWordIndices.txt").toPath(), inputWordEncoded.stream().map(i -> i.toString()).collect(Collectors.toList()));
    Files.write(new File("output/SegmentingWords.txt").toPath(), words.stream().map(word -> word.originalWord).collect(Collectors.toList()));


    displaySortedQualitiesMaps();
    out("allFrags: ");
    out(allFrags);
    out("allWholeWords: ");
    out(allWholeWords);
    out("word count: " + ar.length);
    out("unique word count: " + new HashSet<String>(Arrays.asList(ar)).size());
    out("frags count: ");
    out(allFrags.size());
  }

  private static List<SegmentingWord> convertArrayToProcessedWords(String[] ar) {
    List<SegmentingWord> words = Arrays.stream(ar).map(str -> new SegmentingWord(str)).collect(Collectors.toList());
    return words;
  }

  private static void displaySortedQualitiesMaps() {

    List<Map.Entry<String, Double>> sortedPreQ =
        m_prefix_q
            .entrySet()
            .stream()
            .sorted(Map.Entry.comparingByValue(Comparator.reverseOrder()))
            .collect(Collectors.toList());
    List<Map.Entry<String, Double>> sortedSuffQ =
        m_suffix_q
            .entrySet()
            .stream()
            .sorted(Map.Entry.comparingByValue(Comparator.reverseOrder()))
            .collect(Collectors.toList());
    List<Map.Entry<String, Double>> sortedWordQ =
        m_wholeWord_q
            .entrySet()
            .stream()
            .sorted(Map.Entry.comparingByValue(Comparator.reverseOrder()))
            .collect(Collectors.toList());

    out("");

    out(sortedPreQ);
    out("sortedPreQ");
    out("");
    out(sortedSuffQ);
    out("sortedSuffQ");
    out("");
    out(sortedWordQ);
    out("sortedWordQ");
    out("");

  }

  private static void fillQualitiesMaps() {

    m_prefix_count.entrySet().stream().forEach(stringIntegerEntry -> addToQualitiesMap(m_prefix_q, m_prefixLen_count, m_prefix_count, stringIntegerEntry.getKey(), stringIntegerEntry.getValue()));
    m_suffix_count.entrySet().stream().forEach(stringIntegerEntry -> addToQualitiesMap(m_suffix_q, m_suffixLen_count, m_suffix_count, stringIntegerEntry.getKey(), stringIntegerEntry.getValue()));
    m_wholeWord_count.entrySet().stream().forEach(stringIntegerEntry -> addToQualitiesMap(m_wholeWord_q, m_wholeWordLen_count, m_wholeWord_count, stringIntegerEntry.getKey(), stringIntegerEntry.getValue()));

  }

  private static void fillLenCountsMaps() {

    m_prefix_count.entrySet().stream().forEach(stringIntegerEntry -> addToCountsMap(m_prefixLen_count, stringIntegerEntry.getKey().length()));
    m_suffix_count.entrySet().stream().forEach(stringIntegerEntry -> addToCountsMap(m_suffixLen_count, stringIntegerEntry.getKey().length()));
    m_wholeWord_count.entrySet().stream().forEach(stringIntegerEntry -> addToCountsMap(m_wholeWordLen_count, stringIntegerEntry.getKey().length()));

  }

  private static void displayCountsMaps() {
//    out(m_prefix_count);
//    out("m_prefix_count");
//    out("");
//    out(m_suffix_count);
//    out("m_suffix_count");
//    out("");
//    out(m_wholeWord_count);
//    out("m_wholeWord_count");
//    out("");

    out(m_prefix_count.size());
    out("m_prefix_count.size()");
    out("");
    out(m_suffix_count.size());
    out("m_suffix_count.size()");
    out("");
    out(m_wholeWord_count.size());
    out("m_wholeWord_count.size()");
    out("");

    List<Map.Entry<String, Integer>> sortedPre =
        m_prefix_count
            .entrySet()
            .stream()
            .sorted(Map.Entry.comparingByValue(Comparator.reverseOrder()))
            .collect(Collectors.toList());
    List<Map.Entry<String, Integer>> sortedSuff =
        m_suffix_count
            .entrySet()
            .stream()
            .sorted(Map.Entry.comparingByValue(Comparator.reverseOrder()))
            .collect(Collectors.toList());
    List<Map.Entry<String, Integer>> sortedWord =
        m_wholeWord_count
            .entrySet()
            .stream()
            .sorted(Map.Entry.comparingByValue(Comparator.reverseOrder()))
            .collect(Collectors.toList());

    out(sortedPre);
    out("sortedPre m_prefix_count");
    out("");
    out(sortedSuff);
    out("sortedSuff m_suffix_count");
    out("");
    out(sortedWord);
    out("sortedWord m_wholeWord_count");
    out("");

    out(m_prefixLen_count);
    out("m_prefixLen_count");
    out("");
    out(m_suffixLen_count);
    out("m_suffixLen_count");
    out("");
    out(m_wholeWordLen_count);
    out("m_wholeWordLen_count");
    out("");

  }

  private static void fillCountsMaps(String[] ar) {

    for (String s : ar) {

      //0.  how to handle caps? just lower when putting in map.
      s = s.toLowerCase();
//      out("s: " + s);
      int len = s.length();

//      out("len: " + len);
      //1.  get all prefixes
      //2.  get all suffixes
      //3.  if len <= 4, add to wholeWords

      for (int i = 0; i < maxFragSize && i < len; i++) {
//        out("i: " + i);
        if (i < len - 1) {
          addToCountsMap(m_prefix_count, s.substring(0, i + 1));
          addToCountsMap(m_suffix_count, s.substring(len - i - 1, len));
        }
      }
      if (len <= maxFragSize) {
        addToCountsMap(m_wholeWord_count, s);
      }
    }

  }

  private static String[] getArrayOfCompoundsSplitBeforeSpaceAndPunctuation(String input) throws IOException {

    //1 split around spaces and punctuation.  remove all non-space whitespace
    input = input.replaceAll("[^\\S ]+", " ").trim();
    out(input);

    //surround all spaces and punctuation with: ˧ 	MODIFIER LETTER MID TONE BAR (U+02E7) utf-8 character
    String[] ar = input.split("((?<=[^\\w\\s]|[_ ])|(?=[^\\w\\s]|[_ ]))");
    return ar;
  }

  private static String[] getArrayOfCompoundsSplitBeforeSpaceAndPunctuation(File file) throws IOException {

    String input = new String(Files.readAllBytes(file.toPath()));
    System.out.println(input);

    return getArrayOfCompoundsSplitBeforeSpaceAndPunctuation(input);
  }

  /**
   * also considers whole words per affix quality.
   */
  private static void addToQualitiesMap(Map<String, Double> m_frag_quality, Map<Integer, Integer> m_fragLen_count, Map<String, Integer> m_frag_count, String frag, Integer count) {
    Integer fragLen = frag.length();
    Integer fragLenCount = m_fragLen_count.get(fragLen);

    Integer fragAsWholeWordCount = m_wholeWord_count.containsKey(frag) ? m_wholeWord_count.get(frag) : 0;
    Integer numFragsOfSameLenAsWholeWords = fragAsWholeWordCount > 0 ? m_wholeWordLen_count.get(fragLen) : 0;

    //no
    //quality =  (occurence rate in corpus) / (occurence rate by random probability)

    Double occurrenceRatePerSameLenFrags = count.doubleValue() / fragLenCount.doubleValue();
    Double occurrenceRateByRandomProb = 1.0 / (Math.pow(26, fragLen));
    Integer numUniqueFragsOfSameLen = m_frag_count.size();

    //this is pretty good
    Double quality = Math.pow(fragLen, 2.5) * (count.doubleValue() + fragAsWholeWordCount) / (numUniqueFragsOfSameLen.doubleValue() + numFragsOfSameLenAsWholeWords);//( Math.sqrt(occurrenceRateByRandomProb));

    if (quality >= minQuality) {
      m_frag_quality.put(frag, quality);
    }
  }

  static class SegmentingWord {
    String originalWord;
    String lowercaseWord;
    String currentWord;
    List<String> prefixes;
    List<String> suffixes;
    List<String> remainder;
    List<Integer> capitalizedIndices;
    List<String> segmentedForm;
    List<List<String>> segmentCapitalizationFrags;

    List<String> wholeWordFormCapsChars;

    public String toString() {
      return originalWord + " - " + currentWord + " --- " + prefixes + " --- " + suffixes + " --- <" + remainder + "> -- " + capitalizedIndices;
    }

    public SegmentingWord(String originalWord) {
      this.originalWord = originalWord;
      this.lowercaseWord = originalWord.toLowerCase();
      this.currentWord = lowercaseWord;
      prefixes = new ArrayList<>();
      suffixes = new ArrayList<>();
      remainder = new ArrayList<>();
      capitalizedIndices = new ArrayList<>();
      segmentCapitalizationFrags = new ArrayList<>();

      char[] chars = originalWord.toCharArray();
      for (int i = 0; i < chars.length; i++) {
        if (Character.isUpperCase(chars[i])) {
          capitalizedIndices.add(i);
        }
      }
      Collections.sort(capitalizedIndices, Comparator.reverseOrder());

      process();
      buildSegmentedForm();
      getFinalForm();
      buildWholeWordFormCapsChars();
    }

    private void buildWholeWordFormCapsChars() {
      wholeWordFormCapsChars = new ArrayList<>();
      boolean wholeWordIsCaps = true;

      for (int i = 0; i < originalWord.length(); i++) {
        if (!capitalizedIndices.contains(i)) {
          wholeWordIsCaps = false;
          break;
        }
      }
      if (wholeWordIsCaps) {
        wholeWordFormCapsChars.add(convertIndexToFragCapChar(-1));
        return;
      }

      if (!capitalizedIndices.isEmpty()) {

        //going backwards
        for (int capIndex : capitalizedIndices) {
          String fragCapChar = convertIndexToFragCapChar(capIndex + wholeWordFormCapsChars.size());
          wholeWordFormCapsChars.add(0, fragCapChar);
        }
      }
    }

    private void buildSegmentedForm() {
      segmentedForm = new ArrayList<>();
      segmentedForm.addAll(prefixes);
      segmentedForm.addAll(remainder);
      Collections.reverse(suffixes);
      segmentedForm.addAll(suffixes);

      for (String seg : segmentedForm) {
        segmentCapitalizationFrags.add(new ArrayList<>());
      }

      if (!capitalizedIndices.isEmpty()) {

        //going backwards
        for (int capIndex : capitalizedIndices) {
          //1. determine which frag this index is in.
          //2. save appropriate capitalization frags in appropriate segmentCapitalizationFrags list
          int iter = 0;
          for (int segIndex = 0; segIndex < segmentedForm.size() && segIndex <= capIndex; segIndex++) {
            String seg = segmentedForm.get(segIndex);
            int segLen = seg.length();
            if (capIndex >= iter + segLen) {
              iter += segLen;
              continue;
            } else {
              int fragCapIndex = capIndex - iter;
              String fragCapChar = convertIndexToFragCapChar(fragCapIndex + segmentCapitalizationFrags.get(segIndex).size());
              segmentCapitalizationFrags.get(segIndex).add(0, fragCapChar);
              break;
            }
          }
        }
      }
    }

    private List<String> getFinalForm() {
      List<String> finalForm = new ArrayList<>();

      for (int i = 0; i < segmentedForm.size(); i++) {
        String frag = segmentedForm.get(i);
        List<String> capCharFrags = segmentCapitalizationFrags.get(i);
        for (String c : capCharFrags) {
          finalForm.add(c);
        }
        finalForm.add(frag);
      }
      return finalForm;
    }

    public String output() {
//segmentCapitalizationFrags
      //segmentedForm

      StringBuilder sb = new StringBuilder();
      for (int i = 0; i < segmentedForm.size(); i++) {
        String frag = segmentedForm.get(i);
        List<String> capCharFrags = segmentCapitalizationFrags.get(i);
        for (String c : capCharFrags) {
          sb.append(c);
          sb.append("\n");
        }
        sb.append(frag);
        sb.append("\n");
      }
      return sb.toString();
    }

    private String convertIndexToFragCapChar(int fragCapIndex) {
      /*
      http://www.fileformat.info/info/charset/UTF-8/list.htm
      http://www.fileformat.info/info/charset/UTF-8/list.htm?start=3072

ሏ	ETHIOPIC SYLLABLE LWA (U+120F)	e1888f
ሐ	ETHIOPIC SYLLABLE HHA (U+1210)	e18890
ሑ	ETHIOPIC SYLLABLE HHU (U+1211)	e18891
ሒ	ETHIOPIC SYLLABLE HHI (U+1212)	e18892
ሓ	ETHIOPIC SYLLABLE HHAA (U+1213)	e18893
ሔ	ETHIOPIC SYLLABLE HHEE (U+1214)	e18894
ሕ	ETHIOPIC SYLLABLE HHE (U+1215)	e18895
ሖ	ETHIOPIC SYLLABLE HHO (U+1216)	e18896
ሗ	ETHIOPIC SYLLABLE HHWA (U+1217)	e18897
መ	ETHIOPIC SYLLABLE MA (U+1218)	e18898
ሙ	ETHIOPIC SYLLABLE MU (U+1219)	e18899
       */

      switch (fragCapIndex) {
        case -1: //whole word - all caps
          return "ሏ";
        case 0:
          return "ሐ";
        case 1:
          return "ሑ";
        case 2:
          return "ሒ";
        case 3:
          return "ሓ";
        case 4:
          return "ሔ";
        case 5:
          return "ሕ";
        case 6:
          return "ሖ";
        case 7:
          return "ሗ";
        case 8:
          return "መ";
        case 9:
          return "ሙ";
      }

      return null;
    }


    public void process() {
//      out("processing " + originalWord);
        /*

 1. get all possible prefixes up to 4 letters.  get strongest prefix
2. get all possible suffixes up to 4 letters.  get strongest suffix.
3. if best suffix collides with best prefix, use the stronger one
  - now pick strongest pre or suffix available depending on if left with start or end of word respectively
now that prefix and suffix

     */

      int loop = 0;
      while (currentWord.length() > 0) {
//        out("currentWord: " + currentWord);
        loop++;

        if (currentWord.length() <= maxFragSize) {
          if (m_wholeWord_q.containsKey(currentWord)) {
            remainder.add(currentWord);
            currentWord = "";
            continue;
          }
        }

        List<String> prefixCandidates = new ArrayList<>();
        List<String> suffixCandidates = new ArrayList<>();

        int len = currentWord.length();
        for (int i = 0; i < len && i < maxFragSize; i++) {
          prefixCandidates.add(currentWord.substring(0, i + 1));
          suffixCandidates.add(currentWord.substring(len - i - 1, len));
        }

        if (prefixCandidates.isEmpty() && suffixCandidates.isEmpty()) {
          remainder = currentWord.chars().mapToObj(e -> new Character((char) e).toString()).collect(Collectors.toList());
          currentWord = "";
          continue;
        }

        Double errorValue = -1.0;

        String strongestPre = null;
        Double strongestPreQuality = errorValue;
        String strongestSuf = null;
        Double strongestSufQuality = errorValue;

        for (String frag : prefixCandidates) {
//          Double q = m_prefix_q.get(frag);
//          out("m_prefix_q: " + m_prefix_q);
//          out("frag: " + frag);
          Double q = m_prefix_q.containsKey(frag) ? m_prefix_q.get(frag) : errorValue;
          if (q > strongestPreQuality) {
            strongestPreQuality = q;
            strongestPre = frag;
          }
        }
        for (String frag : suffixCandidates) {
//          out("m_suffix_q: " + m_suffix_q);
//          out("frag: " + frag);
          Double q = m_suffix_q.containsKey(frag) ? m_suffix_q.get(frag) : errorValue;
          if (q > strongestSufQuality) {
            strongestSufQuality = q;
            strongestSuf = frag;
          }
        }
//        if (originalWord.equals(",")) {
//          out("prefixCandidates: " + prefixCandidates);
//          out("suffixCandidates: " + suffixCandidates);
//          out("prefixes: " + prefixes);
//          out("suffixes: " + suffixes);
//        }

        if (strongestSufQuality.equals(errorValue) && strongestPreQuality.equals(errorValue)) {
          remainder = currentWord.chars().mapToObj(e -> new Character((char) e).toString()).collect(Collectors.toList());
          currentWord = "";
          continue;
        }

        //˨	MODIFIER LETTER LOW TONE BAR (U+02E8) utf-8 character
        String tag = "˨˧˦";

        if (strongestPreQuality > strongestSufQuality) {
          prefixes.add(strongestPre);
          currentWord = tag + currentWord;
          currentWord = currentWord.replace(tag + strongestPre, "");
        } else {
          suffixes.add(strongestSuf);
          currentWord = currentWord + tag;
          currentWord = currentWord.replace(strongestSuf + tag, "");
        }
        if (currentWord.contains(tag)) {
          out("");
          out("currentWord");
          out(currentWord);
          out("");
          out("suffixes");
          out(suffixes);
          out("");
          out("prefixes");
          out(prefixes);
          out("");
          out("strongestPre");
          out(strongestPre);
          out("");
          out("strongestSuf");
          out(strongestSuf);
          out("");
          out("strongestPreQuality");
          out(strongestPreQuality);
          out("");
          out("strongestSufQuality");
          out(strongestSufQuality);

          throw new RuntimeException();
        }
      }

    }

    public List<String> getWholeWordFinalForm() {

      List<String> finalWholeWordForm = new ArrayList<>(wholeWordFormCapsChars);
      finalWholeWordForm.add(lowercaseWord);
      return finalWholeWordForm;
    }
  }

  private static <K> void addToCountsMap(Map<K, Integer> map, K key) {
//    out("adding key: " + key);
    Integer currentValue = map.containsKey(key) ? map.get(key) : 0;
    map.put(key, currentValue + 1);
  }
}
////
//          out("");
//          out("currentWord");
//          out(currentWord);
//          out("");
//          out("suffixes");
//          out(suffixes);
//          out("");
//          out("prefixes");
//          out(prefixes);
//          out("");
//          out("strongestPre");
//          out(strongestPreQuality);
//          out("");
//          out("strongestSuf");
//          out(strongestSufQuality);
//          System.exit(0);