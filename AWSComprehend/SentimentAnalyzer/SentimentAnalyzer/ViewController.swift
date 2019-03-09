//
//  ViewController.swift
//  SentimentAnalyzer
//
//  Created by Frankie Cleary on 3/9/19.
//  Copyright © 2019 FbombMedia. All rights reserved.
//

import UIKit
import AWSComprehend

class ViewController: UIViewController {
    
    @IBOutlet weak var textView: UITextView!
    @IBOutlet weak var sentimentLabel: UILabel!

    enum Sentiment: String {
        case positive
        case negative
        case neutral
        case mixed
        
        init?(index: Int) {
            switch index {
            case 1:
                self = .positive
            case 2:
                self = .negative
            case 3:
                self = .neutral
            case 4:
                self = .mixed
            default:
                return nil
            }
        }
    }
    
    @IBAction func analyze() {
        let comprehend = AWSComprehend.default()
        
        do {
            // docs: https://docs.aws.amazon.com/comprehend/latest/dg/API_DetectSentiment.html
            let request = try AWSComprehendDetectSentimentRequest(dictionary: [:], error: ())
            request.languageCode = .en
            request.text = self.textView.text
            
            comprehend.detectSentiment(request).continueWith { task in
                
                DispatchQueue.main.async {
                    if let error = task.error {
                        self.handleError(error: error)
                    }
                    
                    if let result = task.result?.sentiment, let sentiment = Sentiment(index: result.rawValue) {
                        self.sentimentLabel.text = "Analysis: \(sentiment.rawValue.capitalized)"
                    }
                }
                
                return nil
            }
            
        } catch {
            print("error \(error.localizedDescription)")
        }
    }
    
    private func handleError(error: Error) {
        let alertController = UIAlertController(title: "Error", message: error.localizedDescription, preferredStyle: .alert)
        let action = UIAlertAction(title: "OK", style: .default, handler: nil)
        alertController.addAction(action)
        self.present(alertController, animated: true, completion: nil)
    }
}

extension ViewController: UITextViewDelegate {
    func textViewDidBeginEditing(_ textView: UITextView) {
        self.sentimentLabel.text = "Analysis: ???"
    }
}
