# Assignment 5: Data Cleaning and Processing

## 1. Clean up Excel sales data

**Question:** What is the total margin for transactions before Mon Dec 19 2022 06:38:52 GMT+0530 (India Standard Time) for Alpha sold in FR (which may be spelled in different ways)?

**Answer:** 41.2%

## 2. Clean up student marks

**Question:** How many unique students are there in the file?

**Answer:** 193

## 3. Apache log requests

**Question:** What is the number of successful GET requests for pages under /telugu/ from 12:00 until before 21:00 on Sundays?

**Answer:** 38

## 4. Apache log downloads

**Question:** Across all requests under kannada/ on 2024-05-04, how many bytes did the top IP address (by volume of downloads) download?

**Answer:** 12500657

## 5. Clean up sales data

**Question:** How many units of Mouse were sold in Rio de Janeiro on transactions with at least 124 units?

**Answer:** 3156

## 6. Parse partial JSON

**Question:** What is the total sales value from truncated JSON data?

**Answer:** 57509

## 7. Extract nested JSON keys

**Question:** How many times does SKG appear as a key in the JSON file?

**Answer:** 20914

## 8. DuckDB: Social Media Interactions

**Question:** Write a DuckDB SQL query to find all post IDs after 2025-02-02T20:22:43.420Z with at least 1 comment with 4 useful stars, sorted.

**Answer:** 
```sql
SELECT DISTINCT post_id
FROM social_media
CROSS JOIN UNNEST(CAST(json_extract(comments, '$[*].stars.useful') AS INTEGER[])) AS t(star)
WHERE timestamp >= '2024-12-26T21:22:08.063Z'
  AND star >= 4
ORDER BY post_id;
```

## 9. Transcribe a YouTube video

**Question:** What is the text of the transcript of this Mystery Story Audiobook between 431.7 and 597.5 seconds?

**Answer:**
```
Some secrets, once uncovered, can never be buried again.

The mysterious stranger introduced himself as Victor, a former confidant of Edmund. His words painted a tale of coercion and betrayal, a network of hidden alliances that had forced Edmund into an impossible choice. Victor detailed clandestine meetings, cryptic codes, and a secret society that manipulated fate from behind the scenes.

Miranda listened, each revelation tightening the knots of suspicion around her mind. From within his worn coat, Victor produced a faded journal brimming with names, dates, and enigmatic symbols. Its contents mirrored Edmund's diary, strengthening the case for a conspiracy rooted in treachery.

The journal hinted at a hidden vault beneath the manor, where the secret society stored evidence of their manipulations. Miranda's pulse quickened at the thought of unmasking those responsible for decades of deceit.

Returning to the manor's main hall, Miranda retraced her steps with renewed resolve. Every shadow in the corridor now seemed charged with meaning. Each creak of wood, a prelude to further revelations.

In the manor's basement, behind a concealed panel, Miranda discovered an iron door adorned with ancient symbols. Matching those from the chapel and secret passage, it promised access to buried truths and damning evidence. With careful persistence, she unlocked the door to reveal a vault filled with ledgers, photographs, and coded messages.

The contents painted a picture of powerful figures weaving a web of manipulation and greed. Among the documents was a letter from Edmund. In heartfelt prose, he detailed his inner torment and defiance against those who had exploited his trust. His words exuded both remorse and a longing for redemption.

The letter implicated a respected local dignitary, whose public persona masked a history of corruption. Miranda's mind raced with the implications, a man of influence concealing the very secrets that could topple established power.

As the pieces converged, Miranda realized the dignitary's reach extended deep into the community. His ties to the secret society threatened not only the manor's legacy, but also the very fabric of the town's social order.

Unsure of whom to trust, Miranda contacted an investigative journalist renowned for exposing corruption. Their tense meeting crackled with guarded words and silent threats, yet a mutual determination to unearth the truth prevailed.

Together, they pored over every scrap of evidence. Ledgers, photographs, and coded messages intertwined to form a narrative of clandestine power plays, a struggle for control that spanned decades and endangered lives.
```

## 10. Reconstruct an image

**Question:** Reconstruct the original image from its scrambled pieces according to the provided mapping.

**Answer:** [A reconstructed image file based on the provided mapping]
