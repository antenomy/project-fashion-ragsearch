package com.lucas.grant;


import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import org.openqa.selenium.By;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

public class Main {
    // Constants
    private static final String RESULTS_DIR = "results/";
    private static final String PREPROCESSING_FILE = "preprocessing1.txt";
    private static final String NOT_FOUND_FILE = RESULTS_DIR + "not_found_products.txt";
    private static final int WAIT_TIMEOUT_SECONDS = 3;
    private static final int PROCESSING_DELAY_MS = 500;
    private static final String DEFAULT_PRODUCT_ID = "0000000";
    
    // CSS Selectors
    private static final String SEARCH_FIELD_SELECTOR = ".form-control.search";
    private static final String SEARCH_BUTTON_SELECTOR = ".btn.searchIcon";
    private static final String PRODUCT_INFO_TABLE_SELECTOR = ".table.productInfo.mbot_0";
    private static final String SHOW_MORE_BUTTON_SELECTOR = ".showMore.pull-right";
    private static final String INNER_TABLE_SELECTOR = ".innerTable.presentation-table";
    private static final String ARTICLE_DETAILS_TAB_SELECTOR = "a[href='#detailInfo']";
    private static final String NO_PRODUCT_SELECTOR = ".text-center.noProd";
    private static final String ERROR_ALERT_SELECTOR = ".alert.alert-danger";
    
    private static WebDriver driver;
    private static WebDriverWait wait;
    private static ObjectMapper jsonMapper;

    public static void main(String[] args) {
        try {
            initializeComponents();
            List<String> productIds = loadProductIds();
            
            System.out.println("Processing " + productIds.size() + " product IDs...");
            
            ProcessingStats stats = processProducts(productIds);
            printFinalStats(stats);
            
        } catch (Exception e) {
            System.err.println("An error occurred during scraping: " + e.getMessage());
            e.printStackTrace();
        } finally {
            cleanup();
        }
    }

    private static void initializeComponents() {
        System.out.println("Starting product scraper...");
        
        createResultsDirectory();
        setupWebDriver();
        
        jsonMapper = new ObjectMapper();
        jsonMapper.enable(SerializationFeature.INDENT_OUTPUT);
    }

    private static void createResultsDirectory() {
        File directory = new File(RESULTS_DIR);
        if (!directory.exists()) {
            directory.mkdirs();
            System.out.println("Created results directory: " + RESULTS_DIR);
        }
    }
// 1084966
    private static void setupWebDriver() {
        ChromeOptions options = new ChromeOptions();
        String userDataDir = System.getProperty("user.home") + "/selenium-chrome-profile";
        
        options.addArguments(
            "user-data-dir=" + userDataDir,
            // "--headless=new",
            "--window-size=1920,1080",
            "--disable-gpu",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        );

        System.out.println("Launching Chrome (headless mode)");
        driver = new ChromeDriver(options);
        wait = new WebDriverWait(driver, Duration.ofSeconds(WAIT_TIMEOUT_SECONDS));

        driver.get("placeholder.productdomain.com");
        
        System.out.println("If you need to log in, please do so in the browser window.");
        System.out.println("Press Enter when you're ready to continue with the search...");
        new Scanner(System.in).nextLine();
    }

    private static List<String> loadProductIds() {
        try {
            String extractedInfo = Files.readString(Path.of(PREPROCESSING_FILE));
            return Arrays.asList(extractedInfo.split(","));
        } catch (IOException e) {
            System.out.println("Couldn't extract IDs from " + PREPROCESSING_FILE + ": " + e.getMessage());
            System.out.println("Using default product ID: " + DEFAULT_PRODUCT_ID);
            return List.of(DEFAULT_PRODUCT_ID);
        }
    }

    private static ProcessingStats processProducts(List<String> productIds) {
        ProcessingStats stats = new ProcessingStats();
        
        for (int i = 0; i < productIds.size(); i++) {
            String productId = productIds.get(i).trim();

            // Trim ending part of Article ID

            productId = productId.substring(0, 7);
            
            if (isAlreadyProcessed(productId)) {
                stats.skipCount++;
                continue;
            }

            try {
                if (searchForProduct(productId)) {
                    Map<String, Object> productData = extractProductData(productId);
                    saveProductData(productId, productData);
                    stats.successCount++;
                    System.out.println("Success processing product ID " + productId);
                } else {
                    stats.notFoundProducts.add(productId);
                    stats.notFoundCount++;
                }
                
                Thread.sleep(PROCESSING_DELAY_MS);
                
            } catch (Exception e) {
                System.err.println("Error processing product ID " + productId + ": " + e.getMessage());
                stats.errorCount++;
            }
        }
        
        saveNotFoundProducts(stats.notFoundProducts);
        return stats;
    }

    private static boolean isAlreadyProcessed(String productId) {
        File outputFile = new File(RESULTS_DIR + productId + ".json");
        return outputFile.exists();
    }

    private static boolean searchForProduct(String productId) throws Exception {
        // Clear search and enter product ID
        WebElement searchField = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(SEARCH_FIELD_SELECTOR)));
        searchField.clear();
        searchField.sendKeys(productId);

        // Click search
        WebElement searchButton = driver.findElement(By.cssSelector(SEARCH_BUTTON_SELECTOR));
        searchButton.click();

        // Wait for results
        try {
            wait.until(ExpectedConditions.or(
                ExpectedConditions.visibilityOfElementLocated(By.cssSelector(PRODUCT_INFO_TABLE_SELECTOR)),
                ExpectedConditions.visibilityOfElementLocated(By.cssSelector(ERROR_ALERT_SELECTOR)),
                ExpectedConditions.visibilityOfElementLocated(By.cssSelector(NO_PRODUCT_SELECTOR))
            ));

            // Check for no results or error messages
            return driver.findElements(By.cssSelector(NO_PRODUCT_SELECTOR)).isEmpty() && 
                   driver.findElements(By.cssSelector(ERROR_ALERT_SELECTOR)).isEmpty();
                   
        } catch (TimeoutException e) {
            System.out.println("No results found for product ID: " + productId);
            return false;
        }
    }


    // JSON CREATION FUNCTION
    private static Map<String, Object> extractProductData(String productId) throws Exception {
        Map<String, Object> productData = new HashMap<>();
        productData.put("articleId", productId);

        // Extract basic info
        productData.put("basicInfo", extractBasicInfo());
        
        // Extract presentation info (show more section)
        productData.put("presentationInfo", extractPresentationInfo());
        
        // Navigate to article details and extract colors and images
        // navigateToArticleDetails();
        // expandImageSection();

        // productData.put("colors", extractColors(productId));
        Thread.sleep(1500);
        productData.put("variants", extractVariants());

        return productData;
    }




    private static Map<String, String> extractBasicInfo() {
        WebElement productInfoTable = driver.findElement(By.cssSelector(PRODUCT_INFO_TABLE_SELECTOR));
        return extractTableData(productInfoTable);
    }

    private static Map<String, String> extractPresentationInfo() {
        try {
            // Click show more button
            WebElement showMoreButton = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(SHOW_MORE_BUTTON_SELECTOR)));
            showMoreButton.click();
            Thread.sleep(2000);

            // Extract inner table data
            wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector(INNER_TABLE_SELECTOR)));
            WebElement innerTable = driver.findElement(By.cssSelector(INNER_TABLE_SELECTOR));
            return extractTableData(innerTable);
            
        } catch (Exception e) {
            System.out.println("Note: Presentation info could not be processed: " + e.getMessage());
            return new HashMap<>();
        }
    }

    private static Map<String, String> extractTableData(WebElement table) {
        Map<String, String> tableData = new HashMap<>();
        List<WebElement> rows = table.findElements(By.tagName("tr"));
        
        for (WebElement row : rows) {
            List<WebElement> cells = row.findElements(By.tagName("td"));
            if (cells.size() >= 2) {
                String label = cells.get(0).getText().trim();
                String value = cells.get(1).getText().trim();
                if (!label.isEmpty()) {
                    tableData.put(label, value);
                }
            }
        }
        return tableData;
    }



    // ==== MAIN FUNCTION ==== //


    private static Map<String, Object> extractVariants() {
        Map<String, Object> variants = new HashMap<>();

        try {

            List<WebElement> productContainers = driver.findElements(
                By.cssSelector("div.productImg[ng-reflect-klass='productImg']")
            );
            
            for (int i = 0; i < productContainers.size(); i++) {
                Map<String, String> variant = extractProductInfo(productContainers.get(i));
                variants.put(variant.get("variant_code"),variant);
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        }

        return variants;
    }

    private static Map<String, String> extractProductInfo(WebElement productContainer) {
        Map<String, String> variant = new HashMap<>();

        try {
            // Extract image src URL
            WebElement img_element = productContainer.findElement(By.cssSelector("img.clicableImage"));
            String imageSrc = img_element.getAttribute("src");
            variant.put("image_url", imageSrc);
            
            // Extract the full text including the number
            WebElement fullTextElement = productContainer.findElement(
                By.cssSelector("a.articleImagesText")
            );

            String fullText = fullTextElement.getText().trim();
            variant.put("full_text", fullText);
            
            // Extract just the number (assuming it's after the " - ")
            if (fullText.contains("\n- ")) {
                String[] parts = fullText.split("\n- ");
                variant.put("color", parts[0].trim());
                variant.put("variant_code", parts[1].trim());
            } else {
                variant.put("color", "null");
                variant.put("variant_code", "null");
            }
            
        } catch (Exception e) {
            System.out.println("Error extracting product info: " + e.getMessage());
        }
        return variant;
    }



    // =============== //



    private static void navigateToArticleDetails() throws Exception {
        WebElement articleDetailsTab = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(ARTICLE_DETAILS_TAB_SELECTOR)));
        articleDetailsTab.click();
        Thread.sleep(1500);
    }

    private static void expandImageSection() throws Exception {

        List<WebElement> icons = driver.findElements(By.id("colpse1"));

        if (!icons.isEmpty()) {
            WebElement expandIcon = icons.get(0);
            String src = expandIcon.getAttribute("src");

            if (src != null && src.contains("plus.png")) {
                expandIcon.click();
                Thread.sleep(1000);
            }
        }
    }

    private static void saveProductData(String productId, Map<String, Object> productData) throws IOException {
        String filePath = RESULTS_DIR + productId + ".json";
        jsonMapper.writeValue(new File(filePath), productData);
    }

    private static void saveNotFoundProducts(List<String> notFoundProducts) {
        if (notFoundProducts.isEmpty()) return;
        
        try (FileWriter writer = new FileWriter(NOT_FOUND_FILE)) {
            for (String id : notFoundProducts) {
                writer.write(id + "\n");
            }
            System.out.println("Saved list of not found products to " + NOT_FOUND_FILE);
        } catch (IOException e) {
            System.err.println("Failed to save not found products list: " + e.getMessage());
        }
    }

    private static void printFinalStats(ProcessingStats stats) {
        System.out.println("\nProcessing complete!");
        System.out.println("Success: " + stats.successCount);
        System.out.println("Errors: " + stats.errorCount);
        System.out.println("Skipped: " + stats.skipCount);
        System.out.println("Not found: " + stats.notFoundCount);
        
        if (!stats.notFoundProducts.isEmpty()) {
            System.out.println("\nProducts not found: " + String.join(", ", stats.notFoundProducts));
        }
    }

    private static void cleanup() {
        if (driver != null) {
            driver.quit();
            System.out.println("Browser closed.");
        }
    }

    // Helper class for tracking processing statistics
    private static class ProcessingStats {
        int successCount = 0;
        int errorCount = 0;
        int skipCount = 0;
        int notFoundCount = 0;
        List<String> notFoundProducts = new ArrayList<>();
    }
}
