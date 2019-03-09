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
    
    enum Sentiment: String {
        case positive
        case negative
        case neutral
        case mixed
        
        init?(index: Int) {
            switch index {
            case 0:
                self = .positive
            case 1:
                self = .negative
            case 2:
                self = .neutral
            case 3:
                self = .mixed
            default:
                return nil
            }
        }
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        
        let comprehend = AWSComprehend.default()
        
        do {
            // docs: https://docs.aws.amazon.com/comprehend/latest/dg/API_DetectSentiment.html
            let request = try AWSComprehendDetectSentimentRequest(dictionary: [:], error: ())
            request.languageCode = .en
            request.text = "Today it's raining in Seattle"
        
            comprehend.detectSentiment(request).continueWith { task in
                
                if let error = task.error {
                    print("Error occurred: \(error)")
                }
                
                if let result = task.result?.sentiment, let sentiment = Sentiment(index: result.rawValue) {
                    print(sentiment)
                }
                
                return nil
            }
            
        } catch {
            print("error \(error.localizedDescription)")
        }
    }
}
